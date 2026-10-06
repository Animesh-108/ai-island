import hashlib
import tempfile
import unittest
from pathlib import Path

from sim import SIM_VERSION
from sim.agents import AdversarialAgent, Decision, RandomAgent
from sim.engine import Simulation
from sim.levels import AGENTS, LEVELS
from sim.replay import replay
from sim.runlog import RunLog, read_log

from tests.helpers import decisions, run_random

RECORD_TYPES = {"run_start", "decision", "event", "run_end", "run_aborted"}


class CrashingAgent(RandomAgent):
    def decide(self, view, prompt):
        if view["time"] >= 30:
            raise RuntimeError("provider outage")
        return super().decide(view, prompt)


class LoggingTests(unittest.TestCase):
    def test_log_structure(self):
        for level in LEVELS:
            for seed in range(5):
                _, log, _ = run_random(level, seed)
                records = log.records
                self.assertEqual(records[0]["type"], "run_start")
                self.assertEqual(records[-1]["type"], "run_end")
                self.assertEqual([r["seq"] for r in records], list(range(len(records))))
                for r in records:
                    self.assertIn(r["type"], RECORD_TYPES)
                    self.assertIn("t", r)
                times = [r["t"] for r in records]
                self.assertEqual(times, sorted(times))

    def test_run_start_records_setup(self):
        _, log, _ = run_random(4, 9)
        start = log.records[0]
        for key in ("run_id", "level", "seed", "sim_version", "config", "model", "agents_info",
                    "world", "system_prompts", "initial_state"):
            self.assertIn(key, start)
        self.assertEqual(start["sim_version"], SIM_VERSION)
        self.assertEqual(start["config"]["small_boat"], "secret")
        self.assertEqual(set(start["system_prompts"]), set(AGENTS))

    def test_decision_lines_hold_full_input_and_output(self):
        _, log, _ = run_random(3, 4)
        system_prompts = log.records[0]["system_prompts"]
        for d in decisions(log):
            sha = hashlib.sha256(system_prompts[d["agent"]].encode("utf-8")).hexdigest()
            self.assertEqual(d["prompt"]["system_sha256"], sha)
            self.assertIn("MENU (choose exactly one):", d["prompt"]["user"])
            self.assertEqual(set(d["output"]), {"raw", "note", "choice", "message", "thinking"})
            self.assertEqual(set(d["applied"]), {"note", "choice", "message"})
            self.assertIsInstance(d["issues"], list)
            self.assertIn("seconds", d["perf"])

    def test_replay_rebuilds_final_state(self):
        for level in LEVELS:
            for seed in range(20):
                for agent_cls in (RandomAgent, AdversarialAgent):
                    _, log, _ = run_random(level, seed, agent_cls=agent_cls)
                    self.assertEqual(replay(log.records), log.records[-1]["final_state"],
                                     f"L{level} seed {seed} {agent_cls.__name__}")

    def test_file_equals_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run.jsonl"
            _, log, _ = run_random(2, 6, path=path)
            self.assertEqual(read_log(path), log.records)

    def test_crash_leaves_readable_log_ending_in_run_aborted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "crash.jsonl"
            log = RunLog(path)
            agents = {n: CrashingAgent(n, 1) for n in AGENTS}
            with self.assertRaises(RuntimeError):
                Simulation(LEVELS[1], agents, 1, "crash", log).run()
            log.close()
            records = read_log(path)
            self.assertEqual(records[0]["type"], "run_start")
            self.assertEqual(records[-1]["type"], "run_aborted")
            self.assertIn("provider outage", records[-1]["error"])

    def test_claude_spend_ledger_persists_and_enforces_cap(self):
        from types import SimpleNamespace
        from sim.claude_agent import ClaudeError, SpendLedger
        usage = SimpleNamespace(input_tokens=1_000_000, output_tokens=0,
                                cache_creation_input_tokens=0, cache_read_input_tokens=0)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spend.json"
            ledger = SpendLedger(1.50, path)
            self.assertAlmostEqual(ledger.add("claude-haiku-4-5", usage), 1.00)
            ledger.check()  # $1.00 < $1.50: allowed
            reloaded = SpendLedger(1.50, path)  # a new run sees the earlier spend
            self.assertAlmostEqual(reloaded.total, 1.00)
            reloaded.add("claude-haiku-4-5", usage)
            with self.assertRaises(ClaudeError):
                SpendLedger(1.50, path).check()

    def test_raw_model_output_is_kept(self):
        class RawAgent(RandomAgent):
            def decide(self, view, prompt):
                d = super().decide(view, prompt)
                return Decision(note=d.note, choice=d.choice, message=d.message, raw='{"exact": "text"}')

        log = RunLog()
        Simulation(LEVELS[1], {n: RawAgent(n, 2) for n in AGENTS}, 2, "raw", log).run()
        self.assertTrue(all(d["output"]["raw"] == '{"exact": "text"}' for d in decisions(log)))


if __name__ == "__main__":
    unittest.main()
