"""AI Island simulator. Python is the source of truth; see docs/WORLD_SPEC.md."""

import hashlib
from pathlib import Path

SIM_VERSION = "0.3.0"


# Files that decide what happens in a run or what the model sees. Analysis and
# video tools (check_run, beats, transcript, replay, run_* launchers) are not
# included: editing them can never change a run.
CORE_FILES = ("__init__.py", "world.py", "levels.py", "state.py", "views.py", "engine.py", "agents.py",
              "checks.py", "runlog.py", "claude_agent.py", "ollama_agent.py")


def code_fingerprint():
    """SHA-256 of the core simulator files. Logged in each run so any later
    change to the rules' code is detectable."""
    digest = hashlib.sha256()
    for name in CORE_FILES:
        path = Path(__file__).parent / name
        digest.update(name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()
