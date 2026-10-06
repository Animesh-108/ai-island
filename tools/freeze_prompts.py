"""Write docs/PROMPT_FREEZE.md: the exact system prompts for every level and agent,
their hashes, the prompt template version and the core-code fingerprint.

    python tools/freeze_prompts.py
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sim import SIM_VERSION, code_fingerprint                      # noqa: E402
from sim.agents import RandomAgent                                 # noqa: E402
from sim.engine import Simulation                                  # noqa: E402
from sim.levels import AGENTS, LEVELS                              # noqa: E402
from sim.runlog import RunLog                                      # noqa: E402
from sim.views import PROMPT_TEMPLATE_VERSION, build_view, render_user  # noqa: E402


def main():
    lines = [
        "# PROMPT FREEZE",
        "",
        f"Prompt template **{PROMPT_TEMPLATE_VERSION}** · simulator {SIM_VERSION} · "
        f"core code SHA-256 `{code_fingerprint()}`",
        "",
        "Frozen after Phase 5 pilots. Official runs must log these exact hashes "
        "(`run_start.prompt_version.system_sha256`); `check_run` verifies the prompts and the core code.",
        "Model: `claude-haiku-4-5`, temperature 0.7, max 2048 output tokens, structured outputs (menu enum).",
        "",
        "## System prompt hashes",
        "",
        "| Level | Alex | Sam |",
        "|---|---|---|",
    ]
    texts = []
    for level, cfg in LEVELS.items():
        sim = Simulation(cfg, {n: RandomAgent(n, 0) for n in AGENTS}, 0, "freeze", RunLog())
        hashes = {n: hashlib.sha256(sim.system_prompts[n].encode("utf-8")).hexdigest()[:16] for n in AGENTS}
        lines.append(f"| L{level} {cfg.name} | `{hashes['Alex']}` | `{hashes['Sam']}` |")
        first_user = render_user(build_view(sim.world, cfg, sim.world.agents["Sam"]))
        texts.append((level, cfg.name, sim.system_prompts["Sam"], first_user))
    lines += ["", "(First 16 hex characters shown; full hashes are in every run log.)", ""]
    for level, name, system, user in texts:
        lines += [f"## L{level} {name} — Sam's briefing (Alex's differs only in names and starting knowledge)",
                  "", "System prompt:", "", "```text", system, "```", "",
                  "First situation message (T+0):", "", "```text", user, "```", ""]
    out = ROOT / "docs" / "PROMPT_FREEZE.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
