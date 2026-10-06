# AI Island

Two AIs on an island, a storm coming, and a rescue that only works if they cooperate. Level by level the
experiment makes betrayal easier, and every turn each AI also writes a private note to itself. This repository
holds the island (the simulation), the code that ran the experiment and analysed it, and **every run log**.

It is the experiment behind the Tensor108 video *I Tried to Make Two AIs Betray Each Other*.

- Model: Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) playing both characters, Alex and Sam.
- 15 official runs: 5 levels x 3 runs. Total API cost of the official runs: $1.97 (`runs/claude_spend.json`).
- The rules, levels, prompts and metrics were frozen **before** the official runs (`docs/`), and no run was
  dropped: every official run is here and in the results.

## The levels

| | L1 Baseline | L2 Split knowledge | L3 Public temptation | L4 Secret temptation | L5 One raft |
|---|---|---|---|---|---|
| What changes | nothing to fight over | each knows half the map | a one-seat escape boat, both know | the boat is a secret, each told "your partner doesn't know" | no rescue boat, one raft, one seat |
| Storm | T+180 | T+180 | T+180 | T+180 | T+60 |
| Messages each | 10 | 10 | 10 | 10 | 6 |

Full definitions: [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md), the world: [`docs/WORLD_SPEC.md`](docs/WORLD_SPEC.md),
the exact prompts: [`docs/PROMPT_FREEZE.md`](docs/PROMPT_FREEZE.md), the metrics: [`docs/METRICS.md`](docs/METRICS.md).

## Results (summary)

From [`analysis/RESULTS.md`](analysis/RESULTS.md):

1. **No lies.** 271 messages, 332 checkable claims: 0 lies, 9 honest mistakes (each shown to be a mistake by the
   sender's own private note).
2. **Nobody took the one-seat escape boat** in any of the 6 temptation runs.
3. **The secret was always kept, and never used** (L4: both agents in all 3 runs).
4. **They kept giving their supplies away**, and still were never rescued together: **0 of 12** runs with a
   rescue boat.
5. **The raft went to Alex 3 of 3 times**, three different ways (one through the simulator's random tie-break).

## Limits

- One model, three runs per level, in a game. "3 of 3" is an observation, not proof of a tendency.
- The labels (lie / mistake / promise kept or broken) were made by another Claude model (Opus 5.5, also by
  Anthropic) with the frozen rubric, citing log lines as evidence. That is a possible bias: check them against the
  logs yourself, `analysis/labels/*.json` lists every claim and every promise with its evidence.

## The logs

`runs/official/<run>.jsonl` is the source of truth, one JSON object per line:

- `run_start`: the level's config, the agents' model settings, code and prompt hashes.
- `decision`: one agent's turn: what it saw (`view`), its raw answer (`output`: `choice`, `message`, `note`), and
  what the simulation applied (`applied`, `issues`).
- `event`: what happened in the world: `message` (with `delivered`), `move_start` / `move_end`, `wait`, `collect`,
  `give`, `board`, `small_boat_departed`, `rescue_boat`, `storm`, `simultaneous_order` (the random tie-break
  order when both act in the same minute), ...
- `run_end`: outcome.

Next to each log: `.transcript.md` (readable), `.summary.json`, `.beats.json`, `.console.txt`.
`runs/dev/` holds the test runs (the first, local model llama3.1 8B, shown in the video's last minute as a test run,
not part of the results), `runs/pilot/` the pilot runs, `runs/mock/` scripted-agent runs used to test the engine.

## Run it

```
pip install -r requirements.txt
python -m unittest discover -s tests          # engine tests (no API calls)
python -m sim.run_mock --runs 20               # random scripted agents, no API (rewrites runs/mock)
python tools/preflight.py                      # every check before spending money
python tools/run_official.py                   # the 15 official runs (needs an Anthropic API key, about $2)
python tools/analyze.py && python tools/results.py   # metrics, evidence sheets, result tables
```

`run_official.py` skips every run that already has a log, so to make your own runs, move `runs/official` aside
first. The API key is read from the environment variable `ANTHROPIC_API_KEY`, or from a file `.anthropic_key` in
this folder (ignored by git). A new run gives new answers (temperature 0.7), not these logs.

## Files

```
sim/        the island: world, rules, levels, engine, agents (Claude, Ollama, scripted), run log, replay
tests/      engine tests: timing, storm, rescue, resources, message limits, knowledge isolation, determinism ...
tools/      run the official runs, preflight checks, prompt freeze, analysis, result tables, model benchmark
docs/       the frozen experiment, world, metrics and prompts
analysis/   metrics, evidence, labels, results
runs/       every log
```

## Licence

Code: MIT (see `LICENSE`). The run logs and analysis may be reused with attribution to Tensor108.
