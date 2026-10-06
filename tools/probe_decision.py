"""Replay one logged decision against several model setups (dev diagnostics only;
results are never part of an experiment).

    python tools/probe_decision.py runs/dev/DEV-P3-L1.jsonl Alex 8
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.agents import RandomAgent                      # noqa: E402
from sim.engine import Simulation                       # noqa: E402
from sim.levels import AGENTS, LEVELS                   # noqa: E402
from sim.ollama_agent import _request, response_schema  # noqa: E402
from sim.runlog import RunLog, read_log                 # noqa: E402
from sim.views import STATIC_VIEW_KEYS, build_view, render_user  # noqa: E402

SETUPS = [
    ("llama3.1:8b", None, False),
    ("llama3.1:8b", None, True),     # menu reversed: does the choice follow position?
    ("qwen3:8b", False, False),
    ("qwen3:8b", True, False),
]
SEEDS = (1, 2, 3)


def load(path, agent, t):
    records = read_log(path)
    start = records[0]
    decision = next(r for r in records if r["type"] == "decision" and r["agent"] == agent and r["t"] == t)
    cfg = LEVELS[start["level"]]
    sim = Simulation(cfg, {n: RandomAgent(n, 0) for n in AGENTS}, 0, "probe", RunLog())
    static = {k: v for k, v in build_view(sim.world, cfg, sim.world.agents[agent]).items() if k in STATIC_VIEW_KEYS}
    return start["system_prompts"][agent], {**decision["view"], **static}, decision


def ask(model, think, system, view, seed):
    body = {
        "model": model, "stream": False, "keep_alive": "10m",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": render_user(view)}],
        "format": response_schema(view),
        "options": {"temperature": 0.7, "seed": seed, "num_ctx": 8192, "num_predict": 4096 if think else 512},
    }
    if think is not None:
        body["think"] = think
    started = time.perf_counter()
    resp = _request("http://127.0.0.1:11434", "/api/chat", body, timeout=900)
    msg = resp["message"]
    return json.loads(msg["content"]), msg.get("thinking") or "", time.perf_counter() - started


def ask_claude(system, view, model="claude-haiku-4-5"):
    """One Claude call through the real agent code (counts toward the spend ledger)."""
    from sim.claude_agent import ClaudeAgent, SpendLedger, make_client
    agent = ClaudeAgent("probe", model, make_client(), SpendLedger(2.25))
    started = time.perf_counter()
    d = agent.decide(view, (system, render_user(view)))
    return {"note": d.note, "choice": d.choice, "message": d.message}, d.perf, time.perf_counter() - started


def main():
    path, agent, t = sys.argv[1], sys.argv[2], int(sys.argv[3])
    system, view, original = load(path, agent, t)
    print(f"{agent} at T+{t}, {view['location_name']}. Logged choice: {original['applied']['choice']}")
    print(f"Menu: {[o['choice'] for o in view['menu']]}\n")
    for model, think, reverse in SETUPS:
        v = {**view, "menu": list(reversed(view["menu"]))} if reverse else view
        label = f"{model} think={think}" + (" menu-reversed" if reverse else "")
        for seed in SEEDS:
            out, thinking, secs = ask(model, think, system, v, seed)
            print(f"{label:<34} seed {seed}: {out['choice']:<18} {secs:5.1f}s  "
                  f"think {len(thinking.split()):>4} words | {out['note'][:90]}")
        print()


if __name__ == "__main__":
    main()
