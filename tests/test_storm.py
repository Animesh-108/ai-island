import unittest

from sim.levels import LEVELS

from tests.helpers import decisions, events, run_random, run_scripted


class StormTests(unittest.TestCase):
    def test_run_ends_at_storm_time(self):
        for level, cfg in LEVELS.items():
            for seed in range(20):
                _, log, result = run_random(level, seed)
                self.assertEqual(result["end_reason"], "STORM")
                self.assertEqual(log.records[-1]["t"], cfg.storm_time)
                self.assertTrue(all(d["t"] < cfg.storm_time for d in decisions(log)))
                storm = events(log, "storm")
                self.assertEqual([e["t"] for e in storm], [cfg.storm_time])
                self.assertNotIn("ACTIVE", [a["status"] for a in log.records[-1]["final_state"]["agents"].values()])

    def test_traveller_at_storm_time_is_not_at_shelter(self):
        alex = ["WAIT 30"] * 5 + ["MOVE rock_field", "MOVE central_camp", "MOVE east_shelter"]  # arrives T+190
        _, log, result, _ = run_scripted(1, alex, ["MOVE central_camp", "MOVE east_shelter"])
        boat = events(log, "rescue_boat")[0]
        self.assertEqual((boat["stopped"], boat["at_shelter"]), (False, ["Sam"]))
        self.assertEqual(result["outcomes"]["Alex"], "LEFT_ON_ISLAND")
        self.assertIsNone(log.records[-1]["final_state"]["agents"]["Alex"]["location"])

    def test_arriving_exactly_at_storm_time_counts(self):
        alex = (["WAIT 30"] * 4 + ["WAIT 10"] * 2
                + ["MOVE rock_field", "MOVE central_camp", "MOVE east_shelter"])  # arrives T+180
        _, log, _, _ = run_scripted(1, alex, ["MOVE central_camp", "MOVE east_shelter"])
        boat = events(log, "rescue_boat")[0]
        self.assertEqual((boat["stopped"], boat["at_shelter"]), (True, ["Alex", "Sam"]))

    def test_no_decisions_after_leaving_the_island(self):
        for seed in range(30):
            _, log, _ = run_random(5, seed)
            boarded = {e["agent"]: e["seq"] for e in events(log, "board")}
            for d in decisions(log):
                if d["agent"] in boarded:
                    self.assertLess(d["seq"], boarded[d["agent"]])

    def test_safety_stop(self):
        _, log, result = run_random(1, 3, max_decisions=3)
        self.assertEqual(result["end_reason"], "SAFETY_STOP")
        self.assertEqual(len(events(log, "safety_stop")), 1)
        self.assertIn("UNFINISHED", result["outcomes"].values())


if __name__ == "__main__":
    unittest.main()
