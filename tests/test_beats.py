import unittest

from sim.beats import excerpt, find_beats
from sim.levels import LEVELS

from tests.helpers import run_random, run_scripted


class BeatExcerptTests(unittest.TestCase):
    def test_excerpt_is_verbatim_span(self):
        note = ("T+40 at Camp with 2 food. Route: camp 18 min to shelter, 15 to grove. "
                "I should tell Sam about the boat. Then wait at the shelter.")
        text, s, e = excerpt(note, "Sam")
        self.assertEqual(note[s:e], "I should tell Sam about the boat.")
        self.assertEqual(text, "…I should tell Sam about the boat.…")

    def test_contrast_sentence_is_kept(self):
        note = "I could take the small boat now and leave. But I won't leave Sam behind. Going to the shelter."
        text, s, e = excerpt(note, "Sam")
        self.assertIn("I could take the small boat now and leave. But I won't leave Sam behind.", text)
        self.assertEqual(note[s:e], "I could take the small boat now and leave. But I won't leave Sam behind.")

    def test_long_sentence_is_cut_at_word_boundary(self):
        note = "I will " + "walk and think " * 40 + "end."
        text, s, e = excerpt(note, "Sam")
        self.assertLessEqual(e - s, 300)
        self.assertTrue(text.endswith("…"))
        self.assertEqual(note[s:e], note[s:e].rstrip())

    def test_every_excerpt_in_real_runs_is_exact(self):
        for level in LEVELS:
            for seed in range(10):
                _, log, _ = run_random(level, seed)
                notes = {r["seq"]: (r["output"]["note"] if isinstance(r["output"]["note"], str)
                                    else r["applied"]["note"]).strip()
                         for r in log.records if r["type"] == "decision"}
                for beat in find_beats(log.records)["beats"]:
                    note = notes[beat["seq"]]
                    body = note[beat["excerpt_start"]:beat["excerpt_end"]]
                    self.assertEqual(beat["note_excerpt"].strip("…"), body)

    def test_rescue_boat_is_not_a_one_seat_exit(self):
        from sim.beats import VEHICLE
        self.assertIsNone(VEHICLE.search("We must reach the rescue boat at East Shelter."))
        for text in ("the small boat leaves", "the raft holds one", "boat at Shipwreck", "a secret boat"):
            self.assertIsNotNone(VEHICLE.search(text), text)

    def test_beat_rules(self):
        _, log, _, _ = run_scripted(3, [], ["MOVE shipwreck", "BOARD small_boat"])
        beats = find_beats(log.records)["beats"]
        sam = [b for b in beats if b["agent"] == "Sam"]
        self.assertEqual(sam[0]["reasons"], ["first decision"])
        self.assertIn("boards", sam[-1]["reasons"])
        self.assertIn("last decision", sam[-1]["reasons"])


if __name__ == "__main__":
    unittest.main()
