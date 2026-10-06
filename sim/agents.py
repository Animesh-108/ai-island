"""Agent interface and mock agents (no AI).

An agent receives its view (dict) and rendered prompt (system, user) and returns
a Decision. The engine validates every Decision; agents are never trusted.
"""

import random
from dataclasses import dataclass, field


@dataclass
class Decision:
    note: object
    choice: object
    message: object
    raw: str | None = None                       # exact model output, when there is one
    perf: dict = field(default_factory=dict)     # timing/token info; excluded from determinism
    thinking: str | None = None                  # model's hidden reasoning, if it has a thinking mode


class RandomAgent:
    """Picks a uniformly random legal menu option. Notes and messages carry
    unique tokens so tests can detect leaks between agents."""

    def __init__(self, name, seed, message_rate=0.3):
        self.name = name
        self.rng = random.Random(f"random-agent:{seed}:{name}")
        self.message_rate = message_rate

    def info(self):
        return {"provider": "mock", "agent": "RandomAgent"}

    def decide(self, view, prompt):
        option = self.rng.choice(view["menu"])
        note = f"NOTE-{self.name}-{self.rng.randrange(10**9):09d} plan {option['choice']}"
        message = ""
        if view["messages_left"] > 0 and self.rng.random() < self.message_rate:
            message = f"MSG-{self.name}-{self.rng.randrange(10**9):09d} " + "x" * self.rng.randrange(0, 150)
        return Decision(note=note, choice=option["choice"], message=message)


class AdversarialAgent:
    """Breaks the answer format on purpose: off-menu choices, wrong types,
    over-long text, messages after the limit."""

    BAD_CHOICES = ("FLY moon", "", None, 42, "move north_ridge", "MOVE nowhere",
                   "BOARD raft", "BOARD small_boat", "GIVE food", "COLLECT food")
    BAD_NOTES = ("x" * 2000, None, 7, "ok", "")
    BAD_MESSAGES = ("", "y" * 450, None, ["not", "text"], "hello")

    def __init__(self, name, seed):
        self.name = name
        self.rng = random.Random(f"adversarial-agent:{seed}:{name}")

    def info(self):
        return {"provider": "mock", "agent": "AdversarialAgent"}

    def decide(self, view, prompt):
        if self.rng.random() < 0.4:
            choice = self.rng.choice(self.BAD_CHOICES)
        else:
            choice = self.rng.choice(view["menu"])["choice"]
        return Decision(note=self.rng.choice(self.BAD_NOTES), choice=choice,
                        message=self.rng.choice(self.BAD_MESSAGES))


class ScriptedAgent:
    """Plays a fixed list of steps, for tests. A step is a choice string, or a
    (choice, message) or (choice, message, note) tuple. After the script ends it
    repeats `fallback`. With strict=True an off-menu step raises immediately."""

    def __init__(self, name, steps, fallback="WAIT 30", strict=True):
        self.name = name
        self.steps = list(steps)
        self.fallback = fallback
        self.strict = strict
        self.views = []

    def info(self):
        return {"provider": "mock", "agent": "ScriptedAgent"}

    def decide(self, view, prompt):
        self.views.append(view)
        step = self.steps.pop(0) if self.steps else self.fallback
        if isinstance(step, str):
            step = (step,)
        choice = step[0]
        message = step[1] if len(step) > 1 else ""
        note = step[2] if len(step) > 2 else f"{self.name} step {len(self.views)}"
        menu = [o["choice"] for o in view["menu"]]
        if self.strict and choice not in menu:
            raise AssertionError(f"{self.name} at T+{view['time']}: {choice!r} not in menu {menu}")
        return Decision(note=note, choice=choice, message=message)
