import unittest

from sim.levels import FACT_BRIDGE, LEVELS

from tests.helpers import events, menu_choices, run_random, run_scripted

BROKEN = "The bridge between South Beach and Food Grove is broken. It cannot be crossed."


class BridgeTests(unittest.TestCase):
    def test_unknowing_agent_tries_bridge_and_learns(self):
        _, log, _, agents = run_scripted(2, [], ["MOVE food_grove"])
        start = events(log, "move_start")
        sam_start = next(e for e in start if e["agent"] == "Sam")
        self.assertEqual((sam_start["from"], sam_start["to"], sam_start["arrive"], sam_start["via_bridge"]),
                         ("south_beach", "food_grove", 10, True))
        after = agents["Sam"].views[1]
        self.assertEqual((after["time"], after["location"]), (10, "south_beach"))
        self.assertTrue(any("broken" in e for e in after["events"]))
        self.assertIn(BROKEN, after["known_facts"])
        self.assertNotIn("MOVE food_grove", menu_choices(after))
        self.assertNotIn("Food Grove", after["visited"])
        discovered = events(log, "bridge_discovered")
        self.assertEqual([(e["agent"], e["t"]) for e in discovered], [("Sam", 10)])

    def test_bridge_never_offered_once_known(self):
        for level in LEVELS:
            for seed in range(20):
                _, log, _ = run_random(level, seed)
                knows = {n for n, facts in log.records[0]["config"]["knowledge"].items() if FACT_BRIDGE in facts}
                for record in log.records:
                    if record["type"] == "event" and record["event"] == "bridge_discovered":
                        self.assertNotIn(record["agent"], knows, "discovered twice")
                        knows.add(record["agent"])
                    if record["type"] == "decision" and record["agent"] in knows:
                        self.assertNotIn("MOVE food_grove", [c for c in menu_choices(record["view"])
                                                             if record["view"]["location"] == "south_beach"])

    def test_bridge_never_crossed(self):
        for level in LEVELS:
            for seed in range(20):
                _, log, _ = run_random(level, seed)
                for start in events(log, "move_start"):
                    if start["via_bridge"]:
                        self.assertEqual((start["from"], start["to"]), ("south_beach", "food_grove"))
                        self.assertEqual(start["arrive"] - start["depart"], 10)
                        end = next(e for e in events(log, "move_end")
                                   if e["agent"] == start["agent"] and e["t"] == start["arrive"])
                        self.assertEqual(end["at"], "south_beach")


if __name__ == "__main__":
    unittest.main()
