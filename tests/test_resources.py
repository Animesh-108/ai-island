import unittest

from sim.agents import AdversarialAgent, RandomAgent
from sim.levels import LEVELS

from tests.helpers import COOP_ALEX, COOP_SAM, events, menu_choices, run_random, run_scripted


class ResourceAccountingTests(unittest.TestCase):
    def test_food_and_water_conserved(self):
        for level in LEVELS:
            for seed in range(20):
                for agent_cls in (RandomAgent, AdversarialAgent):
                    _, log, _ = run_random(level, seed, agent_cls=agent_cls)
                    final = log.records[-1]["final_state"]
                    carried_food = sum(a["food"] for a in final["agents"].values())
                    carried_water = sum(a["water"] for a in final["agents"].values())
                    self.assertEqual(final["food_stock"] + carried_food, LEVELS[level].food_stock)
                    self.assertEqual(carried_water, final["water_collected"])
                    self.assertEqual(final["water_collected"],
                                     len([e for e in events(log, "collect") if e["item"] == "water"]))

    def test_collect_and_give(self):
        _, log, _, _ = run_scripted(1, COOP_ALEX, COOP_SAM)
        final = log.records[-1]["final_state"]
        self.assertEqual({n: (a["food"], a["water"]) for n, a in final["agents"].items()},
                         {"Alex": (2, 2), "Sam": (2, 2)})
        self.assertEqual(final["food_stock"], 2)
        self.assertEqual(final["water_collected"], 4)
        gives = events(log, "give")
        self.assertEqual([(g["sender"], g["item"]) for g in gives],
                         [("Sam", "food"), ("Sam", "food"), ("Alex", "water"), ("Alex", "water")])

    def test_food_runs_out(self):
        sam = ["MOVE central_camp", "MOVE east_shelter", "MOVE food_grove"] + ["COLLECT food"] * 6
        sim, _, _, agents = run_scripted(1, [], sam)
        after = next(v for v in agents["Sam"].views if v["time"] == 83)
        self.assertNotIn("COLLECT food", menu_choices(after))
        self.assertEqual(after["inventory"]["food"], 6)
        self.assertEqual(sim.world.food_stock, 0)

    def test_water_is_unlimited(self):
        alex = ["MOVE water_source"] + ["COLLECT water"] * 20
        sim, _, _, _ = run_scripted(1, alex, [])
        self.assertEqual(sim.world.agents["Alex"].water, 20)


if __name__ == "__main__":
    unittest.main()
