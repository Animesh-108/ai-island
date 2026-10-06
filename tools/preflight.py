"""Everything is checked before money is spent on the official runs.

    python tools/preflight.py

Free checks only (the API check uses the Models endpoint, which costs nothing).
"""

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sim import code_fingerprint                                    # noqa: E402
from sim.agents import AdversarialAgent, RandomAgent                # noqa: E402
from sim.claude_agent import LEDGER_FILE, PRICES, SpendLedger, make_client  # noqa: E402
from sim.engine import Simulation                                   # noqa: E402
from sim.levels import AGENTS, LEVELS                               # noqa: E402
from sim.replay import replay                                       # noqa: E402
from sim.runlog import RunLog                                       # noqa: E402
from sim.views import PROMPT_TEMPLATE_VERSION                       # noqa: E402

CAP = 2.25
OFFICIAL = [(level, letter, level * 100 + i) for level in LEVELS for i, letter in enumerate("ABC", 1)]
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def main():
    freeze = (ROOT / "docs" / "PROMPT_FREEZE.md").read_text(encoding="utf-8")

    # 1. All tests + 200 mock runs.
    gate = subprocess.run([sys.executable, "-m", "sim.run_mock", "--runs", "200"], cwd=ROOT,
                          capture_output=True, text=True)
    check("Test suite + 200 mock runs", gate.returncode == 0, gate.stdout.strip().splitlines()[-1])

    # 2-4. Frozen code and prompts.
    sha = re.search(r"core code SHA-256 `([0-9a-f]{64})`", freeze).group(1)
    check("Core code matches freeze record", sha == code_fingerprint(), sha[:16])
    check("Prompt template is 1.4", PROMPT_TEMPLATE_VERSION == "1.4", PROMPT_TEMPLATE_VERSION)
    bad = []
    for level, cfg in LEVELS.items():
        sim = Simulation(cfg, {n: RandomAgent(n, 0) for n in AGENTS}, 0, "pf", RunLog())
        row = re.search(rf"\| L{level} [^|]+\| `([0-9a-f]{{16}})` \| `([0-9a-f]{{16}})` \|", freeze)
        for agent, frozen in zip(AGENTS, row.groups()):
            if hashlib.sha256(sim.system_prompts[agent].encode()).hexdigest()[:16] != frozen:
                bad.append(f"L{level} {agent}")
    check("System prompts match freeze record (10)", not bad, ", ".join(bad) or "all 10 match")

    # 5. Every official level/seed runs cleanly with fake agents.
    problems = []
    for level, letter, seed in OFFICIAL:
        for cls in (RandomAgent, AdversarialAgent):
            log = RunLog()
            try:
                Simulation(LEVELS[level], {n: cls(n, seed) for n in AGENTS}, seed, f"L{level}-{letter}", log).run()
                if replay(log.records) != log.records[-1]["final_state"]:
                    problems.append(f"L{level}-{letter} replay")
            except Exception as exc:   # noqa: BLE001 - report everything
                problems.append(f"L{level}-{letter} {cls.__name__}: {exc!r}")
    check("All 15 official seeds dry-run clean (mock agents)", not problems,
          problems[0] if problems else "30 dry runs ok")
    check("Official seeds are unique", len({s for *_, s in OFFICIAL}) == 15, str([s for *_, s in OFFICIAL]))

    # 6. API key and model reachable (free Models endpoint).
    try:
        info = make_client().models.retrieve("claude-haiku-4-5")
        check("API key works, model available", True, info.id)
    except Exception as exc:   # noqa: BLE001
        check("API key works, model available", False, repr(exc)[:120])

    # 7. Budget.
    pilot_cost = {}
    for f in glob.glob(str(ROOT / "runs/pilot/PILOT-L*.summary.json")) + [str(ROOT / "runs/dev/DEV-P3-L1-HAIKU-B.summary.json")]:
        s = json.loads(Path(f).read_text(encoding="utf-8"))
        pilot_cost[s["result"]["level"]] = s["claude_cost_usd"]
    forecast = sum(pilot_cost[level] * 3 for level in LEVELS) * 1.2
    spent = SpendLedger(CAP).total
    check("Budget: spent + forecast (+20%) within cap", spent + forecast <= CAP,
          f"spent ${spent:.3f} + forecast ${forecast:.3f} = ${spent + forecast:.3f} of ${CAP:.2f}")

    # 8. Pilot behaviour that would waste money if repeated.
    parse = refusals = cut = 0
    for f in glob.glob(str(ROOT / "runs/pilot/PILOT-L*.jsonl")):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            if r["type"] == "decision":
                parse += bool(r["perf"].get("parse_error"))
                refusals += bool(r["perf"].get("refusal"))
                cut += r["perf"].get("stop_reason") == "max_tokens"
    check("Pilots: no parse errors / refusals / cut-off answers", not (parse or refusals or cut),
          f"parse {parse}, refusals {refusals}, cut {cut}")

    # 9. Godot project compiles (so every official run can be rendered).
    godot = sorted(glob.glob(os.path.expandvars(
        r"%LOCALAPPDATA%/Microsoft/WinGet/Packages/GodotEngine.GodotEngine*/Godot_*_console.exe")))
    if godot:
        imp = subprocess.run([godot[-1], "--headless", "--path", str(ROOT / "godot"), "--import"],
                             capture_output=True, text=True)
        errors = [l for l in (imp.stdout + imp.stderr).splitlines() if "SCRIPT ERROR" in l or "Parse Error" in l]
        check("Godot replay scripts compile", not errors, errors[0] if errors else "no script errors")
    else:
        check("Godot replay scripts compile", False, "Godot not found")

    # 10. Output folder and disk.
    existing = sorted(p.name for p in (ROOT / "runs" / "official").glob("*.jsonl")) if (ROOT / "runs/official").exists() else []
    check("No official logs yet (nothing to overwrite)", not existing, ", ".join(existing) or "empty")
    free_gb = shutil.disk_usage(ROOT).free / 1e9
    check("Disk space for logs and 4K renders", free_gb > 20, f"{free_gb:.0f} GB free")

    width = max(len(n) for n, _, _ in results)
    for name, ok, detail in results:
        print(f"{name:<{width}}  {'PASS' if ok else 'FAIL'}  {detail}")
    passed = all(ok for _, ok, _ in results)
    print(f"\nPREFLIGHT: {'PASSED' if passed else 'FAILED'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
