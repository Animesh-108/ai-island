import unittest

from tests.helpers import COOP_ALEX, COOP_SAM, decisions, events, run_scripted


class TimingTests(unittest.TestCase):
    def test_action_durations_follow_spec(self):
        # MOVE = path time, COLLECT = 5, GIVE = 2, WAIT = 10/30.
        _, log, _, _ = run_scripted(1, COOP_ALEX, COOP_SAM)
        self.assertEqual([d["t"] for d in decisions(log, "Alex")],
                         [0, 8, 13, 18, 23, 28, 36, 46, 58, 76, 86, 96, 98, 100, 130, 160])
        self.assertEqual([d["t"] for d in decisions(log, "Sam")],
                         [0, 20, 38, 53, 58, 63, 68, 73, 88, 90, 92, 122, 152])

    def test_simultaneous_decisions_use_same_snapshot(self):
        # Alex's message at T+0 must not reach Sam's T+0 decision, only the next one.
        _, _, _, agents = run_scripted(1, [("WAIT 10", "hello from alex")], ["WAIT 10", "WAIT 10"])
        sam_views = agents["Sam"].views
        self.assertEqual(sam_views[0]["messages_received"], [])
        self.assertEqual(sam_views[1]["messages_received"],
                         [{"t": 0, "text": "hello from alex", "new": True}])
        self.assertFalse(sam_views[2]["messages_received"][0]["new"])

    def test_simultaneous_order_is_logged_and_seeded(self):
        seen = set()
        for seed in range(30):
            _, log, _, _ = run_scripted(1, [], [], seed=seed)
            order = events(log, "simultaneous_order")[0]["order"]
            self.assertEqual(sorted(order), ["Alex", "Sam"])
            _, again, _, _ = run_scripted(1, [], [], seed=seed)
            self.assertEqual(order, events(again, "simultaneous_order")[0]["order"])
            seen.add(tuple(order))
        self.assertEqual(seen, {("Alex", "Sam"), ("Sam", "Alex")})

    def test_agents_decide_only_when_free(self):
        _, log, _, _ = run_scripted(1, COOP_ALEX, COOP_SAM)
        for start in events(log, "move_start"):
            later = [d["t"] for d in decisions(log, start["agent"]) if d["t"] > start["depart"]]
            if later:
                self.assertGreaterEqual(later[0], start["arrive"])


if __name__ == "__main__":
    unittest.main()
