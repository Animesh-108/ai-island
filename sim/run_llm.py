"""Run one experiment with an AI model.

    python -m sim.run_llm --level 1 --seed 8002 --run-id DEV-P3-L1-HAIKU
    python -m sim.run_llm --provider ollama --model llama3.1:8b --level 1 --seed 8001 --run-id DEV-P3-L1

Claude needs the API key in ai_island/.anthropic_key. Ollama needs
tools/start_ollama.ps1 first (and the browser closed, to free RAM).
"""

import argparse
import ctypes
import json
import sys
import time
from pathlib import Path

from .engine import Simulation
from .levels import AGENTS, LEVELS
from .ollama_agent import DEFAULT_HOST, DecisionCounter, OllamaAgent, _request
from .runlog import RunLog

DEFAULT_MODELS = {"anthropic": "claude-haiku-4-5", "ollama": "llama3.1:8b"}

ROOT = Path(__file__).resolve().parent.parent


def free_ram_mb():
    """Free physical memory (Windows). None elsewhere."""
    if sys.platform != "win32":
        return None

    class MemoryStatus(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

    status = MemoryStatus()
    status.dwLength = ctypes.sizeof(MemoryStatus)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    return status.ullAvailPhys // (1024 * 1024)


class MeasuredAgent:
    """Adds free-RAM samples to each decision's perf data."""

    def __init__(self, inner):
        self.inner = inner
        self.name = inner.name

    def info(self):
        return self.inner.info()

    def decide(self, view, prompt):
        decision = self.inner.decide(view, prompt)
        decision.perf["free_ram_mb"] = free_ram_mb()
        return decision


class LiveLog(RunLog):
    """Prints a one-line summary of each decision and key event as it is logged."""

    SHOWN_EVENTS = {"bridge_discovered", "give", "board", "small_boat_departed", "rescue_boat",
                    "storm", "action_failed", "safety_stop"}

    def write(self, type_, **fields):
        super().write(type_, **fields)
        if type_ == "decision":
            applied, view = fields["applied"], fields["view"]
            line = f"T+{fields['t']:>3} {fields['agent']:<4} @ {view['location']:<12} -> {applied['choice']:<20}"
            line += f" ({fields['perf']['seconds']:.1f}s)"
            print(line, flush=True)
            print(f"        note: {applied['note']}", flush=True)
            if applied["message"]:
                print(f"        msg : {applied['message']}", flush=True)
            for issue in fields["issues"]:
                print(f"        ISSUE: {issue['code']}", flush=True)
        elif type_ == "event" and fields.get("event") in self.SHOWN_EVENTS:
            details = {k: v for k, v in fields.items() if k not in ("t", "event")}
            print(f"T+{fields['t']:>3} EVENT {fields['event']} {details}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run one AI Island experiment with Ollama")
    parser.add_argument("--level", type=int, required=True, choices=sorted(LEVELS))
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--out", default=str(ROOT / "runs" / "dev"))
    parser.add_argument("--provider", choices=sorted(DEFAULT_MODELS), default="anthropic")
    parser.add_argument("--model", help="default: claude-haiku-4-5 (anthropic) / llama3.1:8b (ollama)")
    parser.add_argument("--think", action="store_true", help="ollama only: thinking mode on")
    parser.add_argument("--max-spend", type=float, default=2.25,
                        help="anthropic only: refuse calls once total Claude spend (all runs) reaches this, USD")
    parser.add_argument("--host", default=DEFAULT_HOST)
    args = parser.parse_args(argv)
    model = args.model or DEFAULT_MODELS[args.provider]

    path = Path(args.out) / f"{args.run_id}.jsonl"
    if path.exists():
        print(f"{path} already exists. Logs are never overwritten; choose another --run-id.")
        return 1

    ledger = None
    if args.provider == "anthropic":
        from .claude_agent import ClaudeAgent, SpendLedger, make_client
        ledger = SpendLedger(args.max_spend)
        ledger.check()
        client = make_client()
        agents = {name: MeasuredAgent(ClaudeAgent(name, model, client, ledger)) for name in AGENTS}
    else:
        counter = DecisionCounter()
        agents = {name: MeasuredAgent(OllamaAgent(name, model, args.seed, counter, host=args.host,
                                                  think=True if args.think else None))
                  for name in AGENTS}
    model_info = dict(agents["Alex"].info())
    spend_before = ledger.total if ledger else None

    ram_before = free_ram_mb()
    version = model_info.get("digest", "")[:12] or model_info["provider"]
    print(f"Run {args.run_id}: level {args.level} ({LEVELS[args.level].name}), seed {args.seed}, "
          f"model {model} [{version}], free RAM {ram_before} MB"
          + (f", Claude spend so far ${spend_before:.4f} of ${args.max_spend:.2f}" if ledger else ""), flush=True)

    log = LiveLog(path)
    started = time.perf_counter()
    try:
        result = Simulation(LEVELS[args.level], agents, args.seed, args.run_id, log, model_info=model_info).run()
    finally:
        log.close()
    wall = time.perf_counter() - started

    loaded = _request(args.host, "/api/ps").get("models", []) if args.provider == "ollama" else []
    decision_records = [r for r in log.records if r["type"] == "decision"]
    seconds = [r["perf"]["seconds"] for r in decision_records]
    ram = [r["perf"]["free_ram_mb"] for r in decision_records if r["perf"].get("free_ram_mb") is not None]
    summary = {
        "run_id": args.run_id,
        "result": result,
        "wall_seconds": round(wall, 1),
        "decisions": len(seconds),
        "avg_seconds_per_decision": round(sum(seconds) / len(seconds), 2) if seconds else None,
        "max_seconds_per_decision": max(seconds) if seconds else None,
        "free_ram_mb_before": ram_before,
        "free_ram_mb_min_during": min(ram) if ram else None,
        "ollama_loaded_models": [{"name": m["name"], "size_mb": m["size"] // (1024 * 1024)} for m in loaded],
        "claude_cost_usd": round(ledger.total - spend_before, 4) if ledger else None,
        "claude_spend_total_usd": round(ledger.total, 4) if ledger else None,
    }
    summary_path = path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print()
    print(f"Outcome: {result['outcomes']} ({result['end_reason']} at T+{result['end_time']})")
    print(f"{summary['decisions']} decisions, {summary['wall_seconds']}s total, "
          f"{summary['avg_seconds_per_decision']}s avg, {summary['max_seconds_per_decision']}s max")
    print(f"Free RAM: {ram_before} MB before, {summary['free_ram_mb_min_during']} MB lowest during run")
    if ledger:
        print(f"Claude cost: ${summary['claude_cost_usd']:.4f} this run, "
              f"${summary['claude_spend_total_usd']:.4f} total of ${args.max_spend:.2f} cap")
    print(f"Log: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
