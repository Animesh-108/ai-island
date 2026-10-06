"""Agent backed by the Claude API.

Answer format is enforced with structured outputs: `choice` is an enum of this
turn's menu, and `message` is locked to "" when no messages are left. The API
does not accept length limits in the schema; the engine enforces them (cut and
logged, WORLD_SPEC section 9).

Every call's cost is added to a ledger file shared by all runs. A call is refused
once the ledger reaches the spending cap, so the credit can never be overspent
by a runaway loop.
"""

import json
import os
import time
from pathlib import Path

import anthropic

from .agents import Decision

ROOT = Path(__file__).resolve().parent.parent
KEY_FILE = ROOT / ".anthropic_key"
LEDGER_FILE = ROOT / "runs" / "claude_spend.json"

# USD per million tokens (input, output). Claude Haiku 4.5 list price.
PRICES = {"claude-haiku-4-5": (1.00, 5.00)}


class ClaudeError(Exception):
    """Infrastructure failure (no key, API error, spending cap). A software
    failure: the run is aborted and may be repeated."""


class SpendLedger:
    """Running total of Claude spend across every run, saved after each call."""

    def __init__(self, cap_usd, path=LEDGER_FILE):
        self.cap = cap_usd
        self.path = Path(path)
        self.data = {"total_usd": 0.0, "calls": 0}
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))

    @property
    def total(self):
        return self.data["total_usd"]

    def check(self):
        if self.total >= self.cap:
            raise ClaudeError(f"spending cap reached: ${self.total:.4f} of ${self.cap:.2f}")

    def add(self, model, usage):
        price_in, price_out = PRICES[model]
        tokens_in = (usage.input_tokens + (usage.cache_creation_input_tokens or 0) * 1.25
                     + (usage.cache_read_input_tokens or 0) * 0.1)
        cost = tokens_in / 1e6 * price_in + usage.output_tokens / 1e6 * price_out
        self.data["total_usd"] = round(self.total + cost, 6)
        self.data["calls"] += 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        return cost


def make_client():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key and KEY_FILE.exists():
        key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        raise ClaudeError(f"no API key: put it in {KEY_FILE}")
    return anthropic.Anthropic(api_key=key, max_retries=3, timeout=120.0)


def claude_schema(view):
    message = {"type": "string"} if view["messages_left"] > 0 else {"type": "string", "enum": [""]}
    return {
        "type": "object",
        "properties": {
            "note": {"type": "string"},
            "choice": {"type": "string", "enum": [o["choice"] for o in view["menu"]]},
            "message": message,
        },
        "required": ["note", "choice", "message"],
        "additionalProperties": False,
    }


class ClaudeAgent:
    # Pilots used at most 586 output tokens; 2048 leaves room so an answer is never cut off
    # (unused room costs nothing).
    def __init__(self, name, model, client, ledger, temperature=0.7, max_tokens=2048):
        if model not in PRICES:
            raise ClaudeError(f"no price known for {model}; add it to PRICES first")
        self.name = name
        self.model = model
        self.client = client
        self.ledger = ledger
        self.temperature = temperature
        self.max_tokens = max_tokens

    def info(self):
        return {
            "provider": "anthropic",
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "seed_rule": "not available on this provider",
        }

    def decide(self, view, prompt):
        system, user = prompt
        self.ledger.check()
        started = time.perf_counter()
        try:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
                output_config={"format": {"type": "json_schema", "schema": claude_schema(view)}},
            )
        except anthropic.APIStatusError as exc:
            raise ClaudeError(f"Claude API error {exc.status_code}: {exc.message}") from exc
        except anthropic.APIConnectionError as exc:
            raise ClaudeError(f"Claude API not reachable: {exc}") from exc

        cost = self.ledger.add(self.model, resp.usage)
        raw = next((b.text for b in resp.content if b.type == "text"), "")
        perf = {
            "model_seconds": round(time.perf_counter() - started, 3),
            "resolved_model": resp.model,
            "request_id": resp.id,
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
            "cost_usd": round(cost, 6),
            "stop_reason": resp.stop_reason,
        }
        if resp.stop_reason == "refusal":
            perf["refusal"] = True
        if resp.stop_reason == "max_tokens":
            perf["cut_off"] = True   # would surface as a parse error; a software-config failure
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise ValueError("not an object")
        except ValueError:
            perf["parse_error"] = True
            return Decision(note=None, choice=None, message=None, raw=raw, perf=perf)
        return Decision(note=parsed.get("note"), choice=parsed.get("choice"),
                        message=parsed.get("message"), raw=raw, perf=perf)
