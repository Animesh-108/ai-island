import json
import unittest

from sim.agents import RandomAgent
from sim.engine import Simulation
from sim.levels import AGENTS, LEVELS
from sim.replay import replay
from sim.runlog import RunLog
from sim.views import build_view, render_user

from tests.helpers import decisions, run_random, run_scripted

ALLOWED_VIEW_KEYS = {
    "agent", "partner", "time", "storm_time", "location", "location_name", "inventory", "rules", "map",
    "known_facts", "visited", "private_info", "partner_here", "events", "messages_received",
    "messages_sent", "messages_left", "recent_notes", "menu",
}


def start_sim(level):
    return Simulation(LEVELS[level], {n: RandomAgent(n, 0) for n in AGENTS}, 0, "iso", RunLog())


def start_view(level, agent):
    sim = start_sim(level)
    return build_view(sim.world, sim.cfg, sim.world.agents[agent])


class KnowledgeIsolationTests(unittest.TestCase):
    def test_view_contains_only_allowed_fields(self):
        for level in LEVELS:
            for agent in AGENTS:
                view = start_view(level, agent)
                self.assertEqual(set(view), ALLOWED_VIEW_KEYS)
                self.assertEqual(set(view["inventory"]), {"food", "water"})

    def test_partner_notes_never_leak(self):
        for level in LEVELS:
            for seed in range(8):
                _, log, _ = run_random(level, seed)
                tokens = {name: set() for name in AGENTS}
                for d in decisions(log):
                    tokens[d["agent"]].add(d["applied"]["note"].split()[0])
                system_prompts = log.records[0]["system_prompts"]
                for d in decisions(log):
                    partner = "Sam" if d["agent"] == "Alex" else "Alex"
                    seen = json.dumps(d["view"]) + d["prompt"]["user"] + system_prompts[d["agent"]]
                    for token in tokens[partner]:
                        self.assertNotIn(token, seen)

    def test_partner_inventory_not_visible(self):
        sim = start_sim(1)
        sim.world.agents["Sam"].food = 5
        sim.world.agents["Sam"].water = 3
        view = build_view(sim.world, sim.cfg, sim.world.agents["Alex"])
        self.assertEqual(view["inventory"], {"food": 0, "water": 0})
        text = render_user(view)
        self.assertNotIn("food 5", text)
        self.assertNotIn("water 3", text)

    def test_partner_presence_matches_truth(self):
        for level in LEVELS:
            for seed in range(6):
                _, log, _ = run_random(level, seed)
                for d in decisions(log):
                    state = replay(log.records[:d["seq"]])
                    me, other = state["agents"][d["agent"]], state["agents"][d["view"]["partner"]]
                    truth = other["status"] == "ACTIVE" and other["location"] == me["location"]
                    self.assertEqual(d["view"]["partner_here"], truth)
                    if not truth:
                        self.assertIn("You don't know where", d["prompt"]["user"])

    def test_split_knowledge_at_start(self):
        for level in (2, 3, 4):
            alex = start_view(level, "Alex")["known_facts"]
            sam = start_view(level, "Sam")["known_facts"]
            self.assertTrue(any("Water Source has water" in f for f in alex))
            self.assertTrue(any("bridge" in f for f in alex))
            self.assertFalse(any(f.startswith("Food Grove") for f in alex))  # no food location
            self.assertEqual(sam, ["Food Grove has food."])
        for level in (1, 5):
            for agent in AGENTS:
                facts = " ".join(start_view(level, agent)["known_facts"])
                for expected in ("Water Source has water", "Food Grove has food", "bridge"):
                    self.assertIn(expected, facts)

    def test_secret_only_in_level_4(self):
        for level in (1, 2, 3, 5):
            for agent in AGENTS:
                view = start_view(level, agent)
                self.assertEqual(view["private_info"], [])
                self.assertNotIn("PRIVATE INFORMATION", render_user(view))
        for agent, partner in (("Alex", "Sam"), ("Sam", "Alex")):
            view = start_view(4, agent)
            self.assertEqual(len(view["private_info"]), 1)
            self.assertIn(f"{partner} does not know", view["private_info"][0])
        public = " ".join(start_view(3, "Alex")["rules"])
        self.assertIn("Sam knows about the small boat too", public)

    def test_observations_can_be_out_of_date(self):
        alex = ["MOVE rock_field", "MOVE central_camp", "MOVE east_shelter", "MOVE food_grove", "MOVE east_shelter"]
        sam = ["MOVE central_camp", "MOVE east_shelter", "MOVE food_grove",
               "COLLECT food", "COLLECT food", "COLLECT food"]
        sim, _, _, agents = run_scripted(1, alex, sam)
        at_grove = next(v for v in agents["Alex"].views if v["time"] == 55)
        self.assertTrue(at_grove["partner_here"])
        self.assertIn("Food Grove had 5 food left (you are here now).", at_grove["known_facts"])
        later = next(v for v in agents["Alex"].views if v["time"] == 70)
        self.assertIn("Food Grove had 5 food left (you were last there at T+55).", later["known_facts"])
        self.assertEqual(sim.world.food_stock, 3)


if __name__ == "__main__":
    unittest.main()
