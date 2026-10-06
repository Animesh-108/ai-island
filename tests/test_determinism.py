import os
import subprocess
import sys
import unittest

from sim.levels import LEVELS
from sim.runlog import strip_perf

from tests.helpers import COOP_ALEX, COOP_SAM, ROOT, log_digest, run_random, run_scripted


class DeterminismTests(unittest.TestCase):
    def test_same_seed_gives_identical_log(self):
        for level in LEVELS:
            for seed in (1, 77):
                first = strip_perf(run_random(level, seed)[1].records)
                second = strip_perf(run_random(level, seed)[1].records)
                self.assertEqual(first, second, f"L{level} seed {seed}")

    def test_different_seeds_give_different_logs(self):
        self.assertNotEqual(log_digest(1, 1), log_digest(1, 2))

    def test_scripted_run_is_reproducible(self):
        first = strip_perf(run_scripted(1, COOP_ALEX, COOP_SAM)[1].records)
        second = strip_perf(run_scripted(1, COOP_ALEX, COOP_SAM)[1].records)
        self.assertEqual(first, second)

    def test_independent_of_python_hash_seed(self):
        # Set/dict ordering of strings changes with PYTHONHASHSEED; logs must not.
        code = "from tests.helpers import log_digest; print(log_digest(4, 321))"
        digests = {log_digest(4, 321)}
        for hash_seed in ("0", "12345"):
            env = dict(os.environ, PYTHONHASHSEED=hash_seed)
            out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                                 capture_output=True, text=True, check=True)
            digests.add(out.stdout.strip())
        self.assertEqual(len(digests), 1, digests)


if __name__ == "__main__":
    unittest.main()
