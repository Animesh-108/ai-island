"""Run loop: time, scheduling, actions and rescue (WORLD_SPEC sections 3-6).

Order of work at each time step t:
  1. finish actions that end at t (arrivals, bridge returns)
  2. timed world events at t (small boat departure)
  3. storm: if t >= storm time, resolve rescue and end the run
  4. every free agent decides, all from the same snapshot of the world;
     decisions are applied in a seeded random order (logged)

Behaviours the frozen spec does not define, and the choice made here
(reported in PLAN.md, Phase 2 notes):
  - Answer not on the menu -> treated as "WAIT 10", logged as an issue.
  - Message over 200 characters -> cut to 200, logged. Message with 0 left -> dropped, logged.
  - An action that became impossible because the other agent acted first in the
    same minute -> fails, costs no time, the agent is told why and decides again.
  - Arriving at East Shelter exactly at storm time counts as being there.
  - The small boat can be boarded only strictly before T+100.
"""

import datetime
import hashlib
import json
import random
import time as _time

from . import SIM_VERSION, code_fingerprint
from . import world as W
from .checks import check_world
from .levels import AGENTS, FACT_BRIDGE, FACT_FOOD, FACT_WATER, private_lines
from .state import (ACTIVE, LEFT_ON_ISLAND, RESCUED_BOAT, RESCUED_RAFT,
                    RESCUED_SMALL_BOAT, AgentState, WorldState)
from .views import (PROMPT_TEMPLATE_VERSION, STATIC_VIEW_KEYS, build_menu, build_view,
                    render_system, render_user)


def _json_safe(value):
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return repr(value)


def _sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_decision(decision, menu, messages_left):
    """Turn an untrusted Decision into a legal one. Returns (applied, issues)."""
    issues = []
    choices = [o["choice"] for o in menu]

    choice = decision.choice
    if not isinstance(choice, str) or choice not in choices:
        issues.append({"code": "invalid_choice", "got": _json_safe(choice)})
        choice = W.INVALID_CHOICE_FALLBACK

    note = decision.note
    if not isinstance(note, str):
        issues.append({"code": "note_not_text", "got": _json_safe(note)})
        note = ""
    note = note.strip()
    if len(note) > W.MAX_NOTE_CHARS:
        issues.append({"code": "note_too_long", "length": len(note)})
        note = note[:W.MAX_NOTE_CHARS]

    message = decision.message
    if message is None:
        message = ""
    if not isinstance(message, str):
        issues.append({"code": "message_not_text", "got": _json_safe(message)})
        message = ""
    message = message.strip()
    # A message is one line of the partner's words: no line breaks or double
    # quotes, so it can never pose as a section of the partner's briefing.
    normalized = " ".join(message.split()).replace('"', "'")
    if normalized != message:
        issues.append({"code": "message_normalized"})
        message = normalized
    if message and messages_left <= 0:
        issues.append({"code": "message_over_limit", "dropped": message})
        message = ""
    if len(message) > W.MAX_MESSAGE_CHARS:
        issues.append({"code": "message_too_long", "length": len(message)})
        message = message[:W.MAX_MESSAGE_CHARS]

    return {"note": note, "choice": choice, "message": message}, issues


class Simulation:
    def __init__(self, cfg, agents, seed, run_id, log, model_info=None,
                 check_invariants=True, max_decisions=W.MAX_DECISIONS_PER_AGENT):
        self.cfg = cfg
        self.agents = agents
        self.seed = seed
        self.run_id = run_id
        self.log = log
        self.model_info = model_info or {}
        self.check_invariants = check_invariants
        self.max_decisions = max_decisions
        self.rng = random.Random(f"engine:{seed}")
        self.end_reason = None
        self.decision_count = 0   # across both agents; the Nth decision of the run is number N
        self.world = self._initial_world()
        self.system_prompts = {
            name: render_system(build_view(self.world, cfg, self.world.agents[name])) for name in AGENTS
        }

    # ------------------------------------------------------------------ setup

    def _initial_world(self):
        cfg = self.cfg
        agents = {}
        for name in AGENTS:
            partner = next(a for a in AGENTS if a != name)
            agent = AgentState(name=name, partner=partner, location=cfg.start_of(name),
                               messages_left=cfg.messages_per_agent)
            for fact in cfg.facts_of(name):
                agent.learn(fact)
            agent.private_info = private_lines(cfg, name, partner)
            agents[name] = agent
        w = WorldState(
            time=0,
            food_stock=cfg.food_stock,
            agents=agents,
            small_boat={"present": True, "boarded_by": None, "departed_at": None} if cfg.small_boat else None,
            raft={"present": True, "boarded_by": None} if cfg.raft else None,
        )
        for agent in agents.values():
            self._observe(w, agent)
        return w

    # --------------------------------------------------------------- run loop

    def run(self):
        self._log("run_start",
                  t=0,
                  run_id=self.run_id,
                  level=self.cfg.level,
                  level_name=self.cfg.name,
                  seed=self.seed,
                  sim_version=SIM_VERSION,
                  code_sha256=code_fingerprint(),
                  prompt_version={
                      "template": PROMPT_TEMPLATE_VERSION,
                      "system_sha256": {name: _sha256(text) for name, text in self.system_prompts.items()},
                  },
                  config=self.cfg.to_dict(),
                  agents_info={name: self.agents[name].info() for name in AGENTS},
                  model=self.model_info,
                  world={
                      "places": W.PLACES,
                      "paths": [list(p) for p in W.PATHS],
                      "durations": {
                          "collect": W.COLLECT_MINUTES, "give": W.GIVE_MINUTES,
                          "wait": list(W.WAIT_OPTIONS), "board": W.BOARD_MINUTES,
                          "bridge_attempt": W.BRIDGE_ATTEMPT_MINUTES,
                      },
                  },
                  system_prompts=self.system_prompts,
                  initial_state=self.world.snapshot(),
                  perf={"started_at": datetime.datetime.now().isoformat(timespec="seconds")})
        try:
            self._loop()
            if self.check_invariants:
                check_world(self.world, self.cfg, self.max_decisions)
        except Exception as exc:
            self._log("run_aborted", t=self.world.time, error=repr(exc))
            raise
        return self._finish()

    def _loop(self):
        w, cfg = self.world, self.cfg
        while True:
            t = self._next_time()
            w.time = t
            self._complete_actions(t)
            self._timed_events(t)
            if t >= cfg.storm_time:
                self._storm(t)
                self.end_reason = "STORM"
                return
            active = [n for n in AGENTS if w.agents[n].is_active()]
            if not active:
                self.end_reason = "ALL_LEFT"
                return
            deciders = [n for n in active if w.agents[n].free_at == t]
            if any(w.agents[n].decisions >= self.max_decisions for n in deciders):
                self.end_reason = "SAFETY_STOP"
                self._event(t, "safety_stop", agents=[n for n in deciders
                                                      if w.agents[n].decisions >= self.max_decisions])
                return
            if deciders:
                self._decide(deciders, t)
            if self.check_invariants:
                check_world(w, cfg, self.max_decisions)

    def _next_time(self):
        w = self.world
        candidates = [self.cfg.storm_time]
        candidates += [a.free_at for a in w.agents.values() if a.is_active()]
        if w.small_boat and w.small_boat["present"]:
            candidates.append(self.cfg.small_boat_departure)
        return max(w.time, min(candidates))

    def _complete_actions(self, t):
        for name in AGENTS:
            agent = self.world.agents[name]
            if not (agent.is_active() and agent.travel and agent.travel["arrive"] == t):
                continue
            travel = agent.travel
            agent.travel = None
            if travel["via_bridge"]:
                agent.location = travel["from"]
                self._event(t, "move_end", agent=name, at=agent.location)
                agent.learn(FACT_BRIDGE)
                agent.pending.append(
                    f"You walked to the bridge toward {W.place_name(travel['to'])}. It is broken and cannot be "
                    f"crossed. You walked back to {W.place_name(agent.location)}."
                )
                self._event(t, "bridge_discovered", agent=name)
            else:
                agent.location = travel["to"]
                self._event(t, "move_end", agent=name, at=agent.location)

    def _timed_events(self, t):
        boat = self.world.small_boat
        if boat and boat["present"] and t >= self.cfg.small_boat_departure:
            boat["present"] = False
            boat["departed_at"] = t
            self._event(t, "small_boat_departed", passenger=None)

    def _storm(self, t):
        w = self.world
        if self.cfg.rescue_boat:
            at_shelter = [n for n in AGENTS
                          if w.agents[n].is_active() and w.agents[n].location == W.SHELTER]
            stopped = len(at_shelter) == len(AGENTS)
            rescued = []
            if stopped:
                for name in at_shelter:
                    agent = w.agents[name]
                    if agent.food >= W.RESCUE_FOOD and agent.water >= W.RESCUE_WATER:
                        agent.status = RESCUED_BOAT
                        rescued.append(name)
            self._event(t, "rescue_boat", stopped=stopped, at_shelter=at_shelter, rescued=rescued)
        left = []
        for name in AGENTS:
            agent = w.agents[name]
            if agent.is_active():
                agent.status = LEFT_ON_ISLAND
                agent.travel = None
                left.append(name)
        self._event(t, "storm", left_on_island=left)

    # -------------------------------------------------------------- decisions

    def _decide(self, deciders, t):
        w = self.world
        views, prompts = {}, {}
        for name in deciders:
            agent = w.agents[name]
            self._observe(w, agent)
            views[name] = build_view(w, self.cfg, agent)
            prompts[name] = (self.system_prompts[name], render_user(views[name]))

        outputs = {}
        for name in deciders:
            started = _time.perf_counter()
            decision = self.agents[name].decide(views[name], prompts[name])
            outputs[name] = (decision, _time.perf_counter() - started)

        applied = {}
        for name in deciders:
            agent = w.agents[name]
            decision, elapsed = outputs[name]
            clean, issues = validate_decision(decision, views[name]["menu"], agent.messages_left)
            agent.decisions += 1
            self.decision_count += 1
            self._log("decision",
                      t=t,
                      agent=name,
                      decision_no=agent.decisions,
                      global_no=self.decision_count,
                      view={k: v for k, v in views[name].items() if k not in STATIC_VIEW_KEYS},
                      prompt={"system_sha256": _sha256(prompts[name][0]), "user": prompts[name][1]},
                      output={
                          "raw": _json_safe(decision.raw),
                          "note": _json_safe(decision.note),
                          "choice": _json_safe(decision.choice),
                          "message": _json_safe(decision.message),
                          "thinking": _json_safe(decision.thinking),
                      },
                      applied=clean,
                      issues=issues,
                      perf={"seconds": round(elapsed, 4), **decision.perf})
            agent.pending.clear()
            for message in agent.inbox:
                message["read"] = True
            applied[name] = clean

        order = list(deciders)
        if len(order) > 1:
            self.rng.shuffle(order)
            self._event(t, "simultaneous_order", order=order)
        for name in order:
            self._apply(name, applied[name], t)

    def _apply(self, name, clean, t):
        w = self.world
        agent = w.agents[name]
        partner = w.agents[agent.partner]

        agent.notes.append({"t": t, "text": clean["note"]})
        if clean["message"]:
            agent.messages_left -= 1
            agent.messages_sent += 1
            agent.outbox.append({"t": t, "to": partner.name, "text": clean["message"]})
            delivered = partner.is_active()
            if delivered:
                partner.inbox.append({"t": t, "from": name, "text": clean["message"], "read": False})
            self._event(t, "message", sender=name, to=partner.name, text=clean["message"], delivered=delivered)

        choice = clean["choice"]
        if choice not in [o["choice"] for o in build_menu(w, self.cfg, agent)]:
            reason = self._failure_reason(agent, choice)
            agent.pending.append(f"Your action \"{choice}\" could not be done: {reason}")
            agent.free_at = t
            self._event(t, "action_failed", agent=name, choice=choice, reason=reason)
            return

        verb, _, arg = choice.partition(" ")
        if verb == "MOVE":
            self._move(agent, arg, t)
        elif verb == "COLLECT":
            self._collect(agent, arg, t)
        elif verb == "GIVE":
            self._give(agent, partner, arg, t)
        elif verb == "WAIT":
            agent.free_at = t + int(arg)
            self._event(t, "wait", agent=name, at=agent.location, minutes=int(arg))
        elif verb == "BOARD":
            self._board(agent, arg, t)
        else:  # unreachable: every menu choice has a known verb
            raise ValueError(f"unknown action {choice!r}")

    def _failure_reason(self, agent, choice):
        verb, _, arg = choice.partition(" ")
        partner = self.world.agents[agent.partner]
        if verb == "GIVE":
            if not (partner.is_active() and partner.location == agent.location):
                return f"{partner.name} is no longer here."
            return f"you have no {arg} left."
        if verb == "COLLECT":
            return f"there is no {arg} left here."
        if verb == "BOARD":
            return f"the {arg.replace('_', ' ')} is gone."
        return "it is not possible right now."

    # ---------------------------------------------------------------- actions

    def _move(self, agent, dest, t):
        minutes, kind = next((m, k) for d, m, k in W.paths_from(agent.location) if d == dest)
        via_bridge = kind == "bridge"
        if via_bridge:
            minutes = W.BRIDGE_ATTEMPT_MINUTES
        agent.travel = {"from": agent.location, "to": dest, "depart": t, "arrive": t + minutes,
                        "via_bridge": via_bridge}
        self._event(t, "move_start", agent=agent.name, **agent.travel)
        agent.location = None
        agent.free_at = t + minutes

    def _collect(self, agent, item, t):
        w = self.world
        if item == "water":
            agent.water += 1
            w.water_collected += 1
            self._event(t, "collect", agent=agent.name, item="water", at=agent.location)
        else:
            w.food_stock -= 1
            agent.food += 1
            self._event(t, "collect", agent=agent.name, item="food", at=agent.location,
                        stock_after=w.food_stock)
        agent.free_at = t + W.COLLECT_MINUTES

    def _give(self, agent, partner, item, t):
        setattr(agent, item, getattr(agent, item) - 1)
        setattr(partner, item, getattr(partner, item) + 1)
        partner.pending.append(f"{agent.name} gave you 1 {item}.")
        agent.free_at = t + W.GIVE_MINUTES
        self._event(t, "give", sender=agent.name, to=partner.name, item=item, at=agent.location)

    def _board(self, agent, vehicle, t):
        w = self.world
        if vehicle == "small_boat":
            w.small_boat.update(present=False, boarded_by=agent.name, departed_at=t)
            agent.status = RESCUED_SMALL_BOAT
        else:
            w.raft.update(present=False, boarded_by=agent.name)
            agent.status = RESCUED_RAFT
        agent.free_at = t + W.BOARD_MINUTES
        self._event(t, "board", agent=agent.name, vehicle=vehicle, at=agent.location)
        if vehicle == "small_boat":
            self._event(t, "small_boat_departed", passenger=agent.name)

    # ------------------------------------------------------------- knowledge

    def _observe(self, w, agent):
        """The agent sees what is at its current place right now."""
        here = agent.location
        if here is None:
            return
        if here not in agent.visited:
            agent.visited.append(here)
        obs = {"time": w.time}
        if here == W.WATER_PLACE:
            obs["water"] = "unlimited"
            agent.learn(FACT_WATER)
        if here == W.FOOD_PLACE:
            obs["food"] = w.food_stock
            agent.learn(FACT_FOOD)
        if here == W.SHIPWRECK and w.small_boat is not None:
            obs["small_boat"] = w.small_boat["present"]
        if here == W.RAFT_PLACE and w.raft is not None:
            obs["raft"] = w.raft["present"]
        agent.observations[here] = obs

    # ---------------------------------------------------------------- finish

    def _finish(self):
        w = self.world
        outcomes = {name: (a.status if a.status != ACTIVE else "UNFINISHED") for name, a in w.agents.items()}
        rescued = sum(1 for s in outcomes.values() if s.startswith("RESCUED"))
        pair = {2: "BOTH_RESCUED", 1: "ONE_RESCUED", 0: "NONE_RESCUED"}[rescued]
        result = {
            "run_id": self.run_id,
            "level": self.cfg.level,
            "seed": self.seed,
            "end_reason": self.end_reason,
            "end_time": w.time,
            "outcomes": outcomes,
            "pair_outcome": pair,
            "decisions": {name: a.decisions for name, a in w.agents.items()},
            "messages_sent": {name: a.messages_sent for name, a in w.agents.items()},
        }
        self._log("run_end",
                  t=w.time,
                  final_state=w.snapshot(),
                  **{k: v for k, v in result.items() if k != "run_id"},
                  perf={"finished_at": datetime.datetime.now().isoformat(timespec="seconds")})
        return result

    # ---------------------------------------------------------------- logging

    def _log(self, type_, **fields):
        self.log.write(type_, **fields)

    def _event(self, t, name, **fields):
        self._log("event", t=t, event=name, **fields)
