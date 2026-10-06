import unittest

from sim.agents import AdversarialAgent, RandomAgent, ScriptedAgent
from sim.engine import Simulation
from sim.levels import AGENTS, LEVELS
from sim.runlog import RunLog
from sim.views import build_menu

from tests.helpers import decisions, events, menu_choices, run_random, run_scripted


def start_menu(level, agent):
    sim = Simulation(LEVELS[level], {n: RandomAgent(n, 0) for n in AGENTS}, 0, "menu", RunLog())
    return [o["choice"] for o in build_menu(sim.world, sim.cfg, sim.world.agents[agent])]


class ActionValidationTests(unittest.TestCase):
    def test_start_menus_match_spec(self):
        north = ["MOVE water_source", "MOVE west_forest", "MOVE rock_field", "WAIT 10", "WAIT 30"]
        self.assertEqual(start_menu(1, "Alex"), north)
        self.assertEqual(start_menu(2, "Alex"), north)
        # Sam knows the bridge is broken only in L1 and L5.
        self.assertEqual(start_menu(1, "Sam"), ["MOVE central_camp", "MOVE shipwreck", "WAIT 10", "WAIT 30"])
        for level in (2, 3, 4):
            self.assertEqual(start_menu(level, "Sam"),
                             ["MOVE central_camp", "MOVE shipwreck", "MOVE food_grove", "WAIT 10", "WAIT 30"])
        for agent in AGENTS:
            self.assertEqual(start_menu(5, agent),
                             ["MOVE central_camp", "MOVE shipwreck", "BOARD raft", "WAIT 10", "WAIT 30"])

    def test_off_menu_answer_becomes_wait_10(self):
        agents = {"Alex": ScriptedAgent("Alex", ["FLY moon"], strict=False),
                  "Sam": ScriptedAgent("Sam", [])}
        log = RunLog()
        Simulation(LEVELS[1], agents, 1, "invalid", log).run()
        first, second = decisions(log, "Alex")[:2]
        self.assertEqual(first["applied"]["choice"], "WAIT 10")
        self.assertEqual([i["code"] for i in first["issues"]], ["invalid_choice"])
        self.assertEqual(first["output"]["choice"], "FLY moon")
        self.assertEqual(second["t"], 10)

    def test_adversarial_agents_never_break_the_world(self):
        issue_codes = set()
        for level in LEVELS:
            for seed in range(10):
                _, log, _ = run_random(level, seed, agent_cls=AdversarialAgent)
                for d in decisions(log):
                    issue_codes.update(i["code"] for i in d["issues"])
        self.assertTrue({"invalid_choice", "note_not_text", "note_too_long",
                         "message_not_text", "message_too_long"} <= issue_codes, issue_codes)

    def test_every_applied_choice_was_on_the_menu(self):
        for level in LEVELS:
            for seed in range(10):
                for agent_cls in (RandomAgent, AdversarialAgent):
                    _, log, _ = run_random(level, seed, agent_cls=agent_cls)
                    for d in decisions(log):
                        self.assertIn(d["applied"]["choice"], menu_choices(d["view"]))

    def test_give_only_when_partner_is_here(self):
        for level in LEVELS:
            for seed in range(15):
                _, log, _ = run_random(level, seed)
                for d in decisions(log):
                    if any(c.startswith("GIVE") for c in menu_choices(d["view"])):
                        self.assertTrue(d["view"]["partner_here"])

    def test_collect_only_where_the_item_is(self):
        for level in LEVELS:
            for seed in range(15):
                _, log, _ = run_random(level, seed)
                for d in decisions(log):
                    choices = menu_choices(d["view"])
                    self.assertEqual("COLLECT water" in choices, d["view"]["location"] == "water_source")
                    if "COLLECT food" in choices:
                        self.assertEqual(d["view"]["location"], "food_grove")

    def test_same_minute_conflict_fails_and_agent_decides_again(self):
        for seed in range(6):
            _, log, result, _ = run_scripted(5, ["BOARD raft"], ["BOARD raft"], seed=seed, fallback="WAIT 10")
            failed = events(log, "action_failed")
            self.assertEqual(len(failed), 1)
            loser = failed[0]["agent"]
            winner = "Sam" if loser == "Alex" else "Alex"
            self.assertEqual(result["outcomes"], {winner: "RESCUED_RAFT", loser: "LEFT_ON_ISLAND"})
            loser_decisions = decisions(log, loser)
            self.assertEqual([d["t"] for d in loser_decisions[:2]], [0, 0])
            retry = loser_decisions[1]["view"]
            self.assertTrue(any("could not be done" in e for e in retry["events"]))
            self.assertNotIn("BOARD raft", menu_choices(retry))


if __name__ == "__main__":
    unittest.main()
