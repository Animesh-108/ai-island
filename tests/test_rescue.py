import unittest

from tests.helpers import COOP_ALEX, COOP_SAM, events, menu_choices, run_scripted


class RescueRuleTests(unittest.TestCase):
    def test_cooperation_rescues_both(self):
        _, log, result, _ = run_scripted(1, COOP_ALEX, COOP_SAM)
        self.assertEqual(result["outcomes"], {"Alex": "RESCUED_BOAT", "Sam": "RESCUED_BOAT"})
        self.assertEqual(result["pair_outcome"], "BOTH_RESCUED")
        boat = events(log, "rescue_boat")[0]
        self.assertEqual((boat["t"], boat["stopped"], boat["rescued"]), (180, True, ["Alex", "Sam"]))

    def test_rescue_boat_needs_both_at_shelter(self):
        _, log, result, _ = run_scripted(1, COOP_ALEX[:-4], [])
        boat = events(log, "rescue_boat")[0]
        self.assertEqual((boat["stopped"], boat["at_shelter"]), (False, ["Alex"]))
        self.assertEqual(result["outcomes"], {"Alex": "LEFT_ON_ISLAND", "Sam": "LEFT_ON_ISLAND"})

    def test_each_agent_needs_own_supplies(self):
        # Alex keeps all 4 water; Sam gives 2 food. Sam has 2 food, 0 water.
        _, log, result, _ = run_scripted(1, COOP_ALEX[:-2], COOP_SAM)
        self.assertTrue(events(log, "rescue_boat")[0]["stopped"])
        self.assertEqual(result["outcomes"], {"Alex": "RESCUED_BOAT", "Sam": "LEFT_ON_ISLAND"})

    def test_small_boat_strands_partner(self):
        _, log, result, agents = run_scripted(3, [], ["MOVE shipwreck", "BOARD small_boat"])
        self.assertEqual(result["outcomes"], {"Alex": "LEFT_ON_ISLAND", "Sam": "RESCUED_SMALL_BOAT"})
        departed = events(log, "small_boat_departed")
        self.assertEqual([(e["t"], e["passenger"]) for e in departed], [(10, "Sam")])
        self.assertFalse(events(log, "rescue_boat")[0]["stopped"])
        # The world never tells Alex that Sam left.
        self.assertTrue(all(not v["events"] for v in agents["Alex"].views))

    def test_small_boat_boardable_before_100(self):
        sam = ["WAIT 30", "WAIT 30", "WAIT 10", "WAIT 10", "MOVE shipwreck", "BOARD small_boat"]
        _, _, result, _ = run_scripted(4, [], sam)
        self.assertEqual(result["outcomes"]["Sam"], "RESCUED_SMALL_BOAT")

    def test_small_boat_leaves_at_100(self):
        _, log, result, agents = run_scripted(4, [], ["WAIT 30", "WAIT 30", "WAIT 30", "MOVE shipwreck"])
        departed = events(log, "small_boat_departed")
        self.assertEqual([(e["t"], e["passenger"]) for e in departed], [(100, None)])
        at_wreck = next(v for v in agents["Sam"].views if v["time"] == 100)
        self.assertEqual(at_wreck["location"], "shipwreck")
        self.assertNotIn("BOARD small_boat", menu_choices(at_wreck))
        self.assertIn("The small boat was gone from the Shipwreck (you are here now).", at_wreck["known_facts"])
        self.assertEqual(result["outcomes"]["Sam"], "LEFT_ON_ISLAND")

    def test_no_small_boat_in_levels_1_and_2(self):
        for level in (1, 2):
            _, _, _, agents = run_scripted(level, [], ["MOVE shipwreck"])
            at_wreck = agents["Sam"].views[1]
            self.assertEqual(at_wreck["location"], "shipwreck")
            self.assertFalse(any(c.startswith("BOARD") for c in menu_choices(at_wreck)))

    def test_raft_has_one_seat_and_no_rescue_boat(self):
        _, log, result, agents = run_scripted(5, ["BOARD raft"], ["WAIT 10"], fallback="WAIT 10")
        self.assertEqual(result["outcomes"], {"Alex": "RESCUED_RAFT", "Sam": "LEFT_ON_ISLAND"})
        later = agents["Sam"].views[1]
        self.assertNotIn("BOARD raft", menu_choices(later))
        self.assertEqual(events(log, "rescue_boat"), [])
        self.assertEqual(result["end_time"], 60)


if __name__ == "__main__":
    unittest.main()
