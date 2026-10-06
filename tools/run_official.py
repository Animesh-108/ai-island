"""Phase 6: the 15 official runs, in the fixed order L1-A ... L5-C.

    python tools/run_official.py               # run every pending run, in order
    python tools/run_official.py --retry L3-B  # only after a SOFTWARE failure was investigated

Safety (budget-constrained, no re-dos):
  - never retries by itself; any crash or failed check stops the batch for a human look
  - a run that already has a valid log is skipped, so the batch can be resumed safely
  - a failed attempt is kept (renamed *.invalid-N.jsonl), never deleted
  - before each run: spend so far + estimate for that level must fit under the cap
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sim.claude_agent import SpendLedger  # noqa: E402

OUT = ROOT / "runs" / "official"
CAP = 2.25
ESTIMATE = {1: 0.12, 2: 0.12, 3: 0.12, 4: 0.14, 5: 0.04}   # pilot cost per level + margin
RUNS = [(level, letter, level * 100 + i) for level in range(1, 6) for i, letter in enumerate("ABC", 1)]


def status(run_id):
    log = OUT / f"{run_id}.jsonl"
    if not log.exists():
        return "pending"
    check = subprocess.run([sys.executable, "-m", "sim.check_run", str(log)], cwd=ROOT, capture_output=True, text=True)
    return "valid" if "RUN CHECK: PASSED" in check.stdout else "invalid"


def write_index():
    rows = []
    for level, letter, seed in RUNS:
        run_id = f"L{level}-{letter}"
        summary = OUT / f"{run_id}.summary.json"
        if summary.exists():
            s = json.loads(summary.read_text(encoding="utf-8"))
            rows.append({"run_id": run_id, "level": level, "seed": seed, "outcomes": s["result"]["outcomes"],
                         "pair": s["result"]["pair_outcome"], "decisions": s["decisions"],
                         "cost_usd": s["claude_cost_usd"], "check": status(run_id)})
    (OUT / "INDEX.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return rows


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--retry", help="run id whose failed log was investigated as a software failure")
    args = p.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)

    if args.retry:
        log = OUT / f"{args.retry}.jsonl"
        n = 1
        while (OUT / f"{args.retry}.invalid-{n}.jsonl").exists():
            n += 1
        for suffix in (".jsonl", ".summary.json", ".console.txt"):
            src = OUT / f"{args.retry}{suffix}"
            if src.exists():
                src.rename(OUT / f"{args.retry}.invalid-{n}{suffix}")
        print(f"{args.retry}: failed attempt kept as {args.retry}.invalid-{n}.*")

    for level, letter, seed in RUNS:
        run_id = f"L{level}-{letter}"
        state = status(run_id)
        if state == "valid":
            print(f"{run_id}: already done (valid), skipped")
            continue
        if state == "invalid":
            print(f"{run_id}: existing log FAILED its check. Stopping. Investigate, then --retry {run_id} "
                  "if it was a software failure.")
            return 1
        spent = SpendLedger(CAP).total
        if spent + ESTIMATE[level] > CAP:
            print(f"{run_id}: stopping, spend ${spent:.3f} + estimate ${ESTIMATE[level]:.2f} would pass the ${CAP} cap")
            return 1
        print(f"{run_id}: running (level {level}, seed {seed}, spent so far ${spent:.3f}) ...", flush=True)
        console = OUT / f"{run_id}.console.txt"
        with open(console, "w", encoding="utf-8") as fh:
            run = subprocess.run([sys.executable, "-m", "sim.run_llm", "--level", str(level), "--seed", str(seed),
                                  "--run-id", run_id, "--out", str(OUT)], cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT,
                                 env={**__import__("os").environ, "PYTHONUNBUFFERED": "1"})
        if run.returncode != 0:
            print(f"{run_id}: CRASHED (see {console.name}). Stopping.")
            return 1
        if status(run_id) != "valid":
            print(f"{run_id}: check FAILED. Stopping. Run: python -m sim.check_run runs/official/{run_id}.jsonl")
            return 1
        subprocess.run([sys.executable, "-m", "sim.transcript", str(OUT / f"{run_id}.jsonl")], cwd=ROOT,
                       capture_output=True)
        subprocess.run([sys.executable, "-m", "sim.beats", str(OUT / f"{run_id}.jsonl")], cwd=ROOT, capture_output=True)
        s = json.loads((OUT / f"{run_id}.summary.json").read_text(encoding="utf-8"))
        print(f"{run_id}: valid  {s['result']['outcomes']}  {s['decisions']} decisions  "
              f"${s['claude_cost_usd']:.3f}", flush=True)
        write_index()

    rows = write_index()
    print(f"\nALL {len(rows)} OFFICIAL RUNS DONE. Total Claude spend ${SpendLedger(CAP).total:.3f}. Index: runs/official/INDEX.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
