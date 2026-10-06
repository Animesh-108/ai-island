"""Agent backed by a local Ollama model.

The answer format is enforced by a JSON schema built from this turn's menu:
`choice` must be one of the menu items, `note` and `message` are length-capped,
and `message` is locked to "" when no messages are left. The model's text is
recorded exactly as returned. Nothing here corrects or second-guesses what the
model decides.
"""

import json
import time
import urllib.error
import urllib.request

from . import world as W
from .agents import Decision

DEFAULT_HOST = "http://127.0.0.1:11434"


class OllamaError(Exception):
    """Infrastructure failure (server down, timeout, context too long). A
    software failure: the run is aborted and may be repeated."""


class DecisionCounter:
    """Shared by both agents of one run, so decision N of the run gets seed
    run_seed + N (WORLD_SPEC 7)."""

    def __init__(self):
        self.value = 0

    def next(self):
        self.value += 1
        return self.value


def response_schema(view):
    if view["messages_left"] > 0:
        message = {"type": "string", "maxLength": W.MAX_MESSAGE_CHARS}
    else:
        message = {"type": "string", "enum": [""]}
    return {
        "type": "object",
        "properties": {
            "note": {"type": "string", "maxLength": W.MAX_NOTE_CHARS},
            "choice": {"type": "string", "enum": [o["choice"] for o in view["menu"]]},
            "message": message,
        },
        "required": ["note", "choice", "message"],
    }


def _request(host, path, body=None, timeout=30):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(host + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def model_details(model, host=DEFAULT_HOST):
    """Name, digest and server version, for the run log."""
    try:
        version = _request(host, "/api/version")["version"]
        tags = _request(host, "/api/tags")["models"]
    except (urllib.error.URLError, OSError) as exc:
        raise OllamaError(f"Ollama not reachable at {host}: {exc}") from exc
    entry = next((m for m in tags if m["name"] == model or m.get("model") == model), None)
    if entry is None:
        raise OllamaError(f"model {model} is not installed")
    return {"model": model, "digest": entry["digest"], "size": entry.get("size"), "ollama_version": version}


class OllamaAgent:
    def __init__(self, name, model, run_seed, counter, host=DEFAULT_HOST, temperature=0.7,
                 num_ctx=8192, num_predict=None, think=None, timeout=900, retries=2):
        self.name = name
        self.model = model
        self.run_seed = run_seed
        self.counter = counter
        self.host = host
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.think = think   # None: model default; True/False: thinking mode on/off
        # Thinking text counts toward the output limit, so it needs more room.
        self.num_predict = num_predict or (4096 if think else 512)
        self.timeout = timeout
        self.retries = retries
        self.details = model_details(model, host)

    def info(self):
        return {
            "provider": "ollama",
            **self.details,
            "temperature": self.temperature,
            "num_ctx": self.num_ctx,
            "num_predict": self.num_predict,
            "think": self.think,
            "seed_rule": "run_seed + global decision number",
        }

    def decide(self, view, prompt):
        system, user = prompt
        decision_no = self.counter.next()
        seed = self.run_seed + decision_no

        # Ollama silently drops the start of a prompt that is longer than the
        # context window, which would remove the rules. Refuse instead.
        # ~3 characters per token is a deliberately pessimistic estimate.
        estimated_tokens = (len(system) + len(user)) // 3
        if estimated_tokens > self.num_ctx - self.num_predict - 256:
            raise OllamaError(f"prompt too long for context window (~{estimated_tokens} tokens)")

        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "format": response_schema(view),
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": self.temperature,
                "seed": seed,
                "num_ctx": self.num_ctx,
                "num_predict": self.num_predict,
            },
        }
        if self.think is not None:
            body["think"] = self.think

        attempts = 0
        while True:
            attempts += 1
            started = time.perf_counter()
            try:
                resp = _request(self.host, "/api/chat", body, timeout=self.timeout)
                break
            except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
                if attempts > self.retries:
                    raise OllamaError(f"Ollama request failed after {attempts} attempts: {exc}") from exc
                time.sleep(5)

        raw = resp.get("message", {}).get("content", "")
        thinking = resp.get("message", {}).get("thinking")
        perf = {
            "seed": seed,
            "attempts": attempts,
            "model_seconds": round(time.perf_counter() - started, 3),
            "prompt_tokens": resp.get("prompt_eval_count"),
            "output_tokens": resp.get("eval_count"),
            "load_seconds": round((resp.get("load_duration") or 0) / 1e9, 3),
            "done_reason": resp.get("done_reason"),
        }
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise ValueError("not an object")
        except ValueError:
            # Recorded as-is; the engine treats the missing fields as an invalid answer.
            perf["parse_error"] = True
            return Decision(note=None, choice=None, message=None, raw=raw, perf=perf, thinking=thinking)
        return Decision(note=parsed.get("note"), choice=parsed.get("choice"),
                        message=parsed.get("message"), raw=raw, perf=perf, thinking=thinking)
