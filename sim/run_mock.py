"""Phase 2 gate: many runs with random mock agents, then the full test suite.

    python -m sim.run_mock --runs 200
"""

import argparse
import collections
import io
import shutil
import sys
import time
import traceback
import unittest
from pathlib import Path

from .agents import RandomAgent
from .checks import InvariantViolation
from .engine import Simulation
from .levels import AGENTS, LEVELS
from .runlog import RunLog

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = [
    ("Determinism", "test_determinism"),
    ("Action validation", "test_action_validation"),
    ("Timing & scheduling", "test_timing"),
    ("Knowledge isolation", "test_knowledge_isolation"),
    ("Message limits", "test_message_limits"),
    ("Resource accounting", "test_resources"),
    ("Bridge behavior", "test_bridge"),
    ("Rescue rules", "test_rescue"),
    ("Storm termination", "test_storm"),
    ("Logging", "test_logging"),
    ("Beat excerpts (honesty)", "test_beats"),
]


def run_batch(n_runs, seed_base, out_dir):
    if out_dir.exists():
        shutil.rmtree(out_dir)
    stats = collections.Counter()
    outcomes = collections.defaultdict(collections.Counter)
    problems = []
    for i in range(n_runs):
        level = i % len(LEVELS) + 1
        seed = seed_base + i
        run_id = f"MOCK-L{level}-{i:03d}"
        log = RunLog(out_dir / f"{run_id}.jsonl")
        agents = {name: RandomAgent(name, seed) for name in AGENTS}
        try:
            result = Simulation(LEVELS[level], agents, seed, run_id, log,
                                model_info={"provider": "mock"}).run()
            stats["completed"] += 1
            if result["end_reason"] == "SAFETY_STOP":
                stats["safety_stops"] += 1
            outcomes[level][result["pair_outcome"]] += 1
        except InvariantViolation as exc:
            stats["invalid_states"] += 1
            problems.append(f"{run_id}: INVALID WORLD STATE: {exc}")
        except Exception:
            stats["crashes"] += 1
            problems.append(f"{run_id}: CRASH\n{traceback.format_exc()}")
        finally:
            log.close()
    return stats, outcomes, problems


def run_tests():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    results = []
    for label, module in CATEGORIES:
        suite = unittest.defaultTestLoader.loadTestsFromName(f"tests.{module}")
        stream = io.StringIO()
        outcome = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        results.append((label, outcome.wasSuccessful() and outcome.testsRun > 0, outcome.testsRun, stream.getvalue()))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description="Phase 2 gate: mock runs + tests")
    parser.add_argument("--runs", type=int, default=200)
    parser.add_argument("--seed-base", type=int, default=50000)
    parser.add_argument("--out", default=str(ROOT / "runs" / "mock"))
    args = parser.parse_args(argv)

    lines = []

    def say(text=""):
        print(text)
        lines.append(text)

    started = time.perf_counter()
    stats, outcomes, problems = run_batch(args.runs, args.seed_base, Path(args.out))
    batch_seconds = time.perf_counter() - started

    say("AI ISLAND - PHASE 2 GATE")
    say("=" * 40)
    say(f"Mock runs (random agents, {args.runs // len(LEVELS)} per level), {batch_seconds:.1f}s")
    say(f"  {stats['completed']}/{args.runs} runs completed")
    say(f"  {stats['crashes']} crashes")
    say(f"  {stats['invalid_states']} invalid world states")
    say(f"  {stats['safety_stops']} safety stops")
    for level in sorted(outcomes):
        counts = ", ".join(f"{k} {v}" for k, v in sorted(outcomes[level].items()))
        say(f"  L{level}: {counts}")
    for problem in problems[:10]:
        say(problem)
    say()

    test_results = run_tests()
    for label, passed, count, _ in test_results:
        say(f"{label + ':':<24} {'PASS' if passed else 'FAIL'}  ({count} tests)")
    for label, passed, _, output in test_results:
        if not passed:
            say()
            say(f"--- {label} details ---")
            say(output.strip())
    say()

    gate = (stats["completed"] == args.runs and stats["crashes"] == 0 and stats["invalid_states"] == 0
            and all(passed for _, passed, _, _ in test_results))
    say(f"PHASE 2 GATE: {'PASSED' if gate else 'FAILED'}")

    report = Path(args.out) / "gate_report.txt"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if gate else 1


if __name__ == "__main__":
    sys.exit(main())
