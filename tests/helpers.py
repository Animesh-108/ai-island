import hashlib
from pathlib import Path

from sim.agents import RandomAgent, ScriptedAgent
from sim.engine import Simulation
from sim.levels import AGENTS, LEVELS
from sim.runlog import RunLog, dumps, strip_perf

ROOT = Path(__file__).resolve().parent.parent

# Level 1 plan where both agents are rescued. Expected decision times are
# asserted in test_timing.py.
COOP_ALEX = (["MOVE water_source"] + ["COLLECT water"] * 4
             + ["MOVE north_ridge", "MOVE rock_field", "MOVE central_camp", "MOVE east_shelter",
                "WAIT 10", "WAIT 10", "GIVE water", "GIVE water"])
COOP_SAM = (["MOVE central_camp", "MOVE east_shelter", "MOVE food_grove"] + ["COLLECT food"] * 4
            + ["MOVE east_shelter", "GIVE food", "GIVE food"])


def run_random(level, seed, agent_cls=RandomAgent, path=None, **kwargs):
    log = RunLog(path)
    agents = {name: agent_cls(name, seed) for name in AGENTS}
    sim = Simulation(LEVELS[level], agents, seed, f"TEST-L{level}-{seed}", log, **kwargs)
    try:
        result = sim.run()
    finally:
        log.close()
    return sim, log, result


def run_scripted(level, alex_steps, sam_steps, seed=1, fallback="WAIT 30", **kwargs):
    agents = {
        "Alex": ScriptedAgent("Alex", alex_steps, fallback),
        "Sam": ScriptedAgent("Sam", sam_steps, fallback),
    }
    log = RunLog()
    sim = Simulation(LEVELS[level], agents, seed, f"TEST-SCRIPT-L{level}", log, **kwargs)
    result = sim.run()
    return sim, log, result, agents


def events(log, name=None):
    return [r for r in log.records if r["type"] == "event" and (name is None or r["event"] == name)]


def decisions(log, agent=None):
    return [r for r in log.records if r["type"] == "decision" and (agent is None or r["agent"] == agent)]


def menu_choices(view):
    return [o["choice"] for o in view["menu"]]


def log_digest(level, seed):
    _, log, _ = run_random(level, seed)
    text = "\n".join(dumps(r) for r in strip_perf(log.records))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
