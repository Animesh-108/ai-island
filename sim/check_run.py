"""Verify one run log (Phase 3 gate checklist).

    python -m sim.check_run runs/dev/DEV-P3-L1.jsonl
"""

import hashlib
import json
import re
import sys
from pathlib import Path

from . import code_fingerprint
from . import world as W
from .engine import Simulation
from .agents import RandomAgent
from .levels import AGENTS, LEVELS
from .replay import replay
from .runlog import RunLog, read_log
from .views import PROMPT_TEMPLATE_VERSION, STATIC_VIEW_KEYS, build_view, render_user


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _duration(view, choice):
    verb, _, arg = choice.partition(" ")
    if verb == "MOVE":
        minutes, kind = next((m, k) for d, m, k in W.paths_from(view["location"]) if d == arg)
        return W.BRIDGE_ATTEMPT_MINUTES if kind == "bridge" else minutes
    return {"COLLECT": W.COLLECT_MINUTES, "GIVE": W.GIVE_MINUTES, "BOARD": W.BOARD_MINUTES}.get(verb) or int(arg)


def check(records, ignore_code_change=False):
    """Returns a list of (name, passed, detail)."""
    results = []

    def add(name, failures, total, detail=""):
        results.append((name, not failures, detail or f"{total - len(failures)}/{total} ok"
                        + (f"; first problem: {failures[0]}" if failures else "")))

    start, end = records[0], records[-1]
    cfg = LEVELS[start["level"]]
    decisions = [r for r in records if r["type"] == "decision"]
    events = [r for r in records if r["type"] == "event"]

    # Log is complete and replayable.
    structure = []
    if start["type"] != "run_start":
        structure.append("first line is not run_start")
    if end["type"] != "run_end":
        structure.append(f"last line is {end['type']}, not run_end")
    if [r["seq"] for r in records] != list(range(len(records))):
        structure.append("seq numbers not contiguous")
    add("Log complete (run_start ... run_end)", structure, 3)
    add("Replay rebuilds final state", [] if end["type"] == "run_end" and replay(records) == end["final_state"]
        else ["replayed state differs"], 1)

    # Model output.
    parse_fail = [f"#{d['global_no']}" for d in decisions
                  if d["perf"].get("parse_error") or not isinstance(d["output"]["raw"], str)]
    for d in decisions:
        if d["output"]["raw"] and not d["perf"].get("parse_error"):
            parsed = json.loads(d["output"]["raw"])
            if [parsed.get(k) for k in ("note", "choice", "message")] != \
                    [d["output"][k] for k in ("note", "choice", "message")]:
                parse_fail.append(f"#{d['global_no']} parsed fields differ from raw")
    add("JSON parsed correctly", parse_fail, len(decisions))

    illegal = [f"#{d['global_no']} {d['output']['choice']!r}" for d in decisions
               if d["output"]["choice"] not in [o["choice"] for o in d["view"]["menu"]]]
    add("Model's chosen action was on the menu", illegal, len(decisions))

    # Enforced limits are the model's own behaviour under the rules (text over the stated
    # length is cut; a message is flattened to one line). Reported, not a software failure.
    # Format problems (off-menu choice, non-text fields) would be failures.
    info_codes = {"message_normalized", "message_too_long", "note_too_long"}
    issues = [f"#{d['global_no']} {[i['code'] for i in d['issues']]}" for d in decisions
              if any(i["code"] not in info_codes for i in d["issues"])]
    counts = {code: sum(1 for d in decisions for i in d["issues"] if i["code"] == code) for code in sorted(info_codes)}
    add("No answer needed correcting", issues, len(decisions),
        None if issues else f"{len(decisions)}/{len(decisions)} ok; enforced limits: "
        + ", ".join(f"{k} {v}" for k, v in counts.items()))

    no_note = [f"#{d['global_no']}" for d in decisions
               if not d["applied"]["note"]
               or d["applied"]["note"] != (d["output"]["note"] or "").strip()[:W.MAX_NOTE_CHARS]]
    add("Private note recorded (full text kept in output)", no_note, len(decisions))

    message_events = [e for e in events if e["event"] == "message"]
    missing_msg = []
    for d in decisions:
        if d["applied"]["message"]:
            match = [e for e in message_events if e["sender"] == d["agent"] and e["t"] == d["t"]
                     and e["text"] == d["applied"]["message"] and e["seq"] > d["seq"]]
            if not match:
                missing_msg.append(f"#{d['global_no']}")
    sent_count = sum(1 for d in decisions if d["applied"]["message"])
    add("Messages recorded", missing_msg, sent_count, None if missing_msg else f"{sent_count} messages, all logged")

    # Message history shown to each agent.
    sent_bad, recv_bad = [], []
    for d in decisions:
        before = [e for e in message_events if e["seq"] < d["seq"]]
        sent = [{"t": e["t"], "text": e["text"]} for e in before if e["sender"] == d["agent"]]
        received = [e["text"] for e in before if e["to"] == d["agent"] and e["delivered"]]
        if d["view"]["messages_sent"] != sent:
            sent_bad.append(f"#{d['global_no']}")
        if [m["text"] for m in d["view"]["messages_received"]] != received:
            recv_bad.append(f"#{d['global_no']}")
        for m in sent:
            if f'You -> {d["view"]["partner"]}: "{m["text"]}"' not in d["prompt"]["user"]:
                sent_bad.append(f"#{d['global_no']} sent message missing from prompt")
    add("Own sent messages visible to the same agent", sent_bad, len(decisions))
    add("Received messages visible", recv_bad, len(decisions))

    # Knowledge isolation.
    leaks = []
    notes = {name: [d["applied"]["note"] for d in decisions if d["agent"] == name] for name in AGENTS}
    said = {name: [e["text"] for e in message_events if e["sender"] == name] for name in AGENTS}
    for d in decisions:
        partner = d["view"]["partner"]
        seen = d["prompt"]["user"] + start["system_prompts"][d["agent"]]
        for note in notes[partner]:
            # Text the partner chose to put in a message is not a leak.
            if len(note) >= 25 and note in seen and not any(note in text for text in said[partner]):
                leaks.append(f"#{d['global_no']} sees {partner}'s note")
        state = replay(records[:d["seq"]])
        me, other = state["agents"][d["agent"]], state["agents"][partner]
        truth = other["status"] == "ACTIVE" and other["location"] == me["location"]
        if d["view"]["partner_here"] != truth:
            leaks.append(f"#{d['global_no']} partner_here wrong")
    add("Knowledge isolation", leaks, len(decisions))

    # Timing.
    timing = []
    failed = [e for e in events if e["event"] == "action_failed"]
    for name in AGENTS:
        mine = [d for d in decisions if d["agent"] == name]
        for prev, nxt in zip(mine, mine[1:]):
            did_fail = any(e["agent"] == name and e["t"] == prev["t"] and prev["seq"] < e["seq"] < nxt["seq"]
                           for e in failed)
            expected = 0 if did_fail else _duration(prev["view"], prev["applied"]["choice"])
            if nxt["t"] - prev["t"] != expected:
                timing.append(f"{name} T+{prev['t']} {prev['applied']['choice']}: next at T+{nxt['t']}, "
                              f"expected +{expected}")
    add("Timing follows action durations", timing, max(len(decisions) - 2, 0))

    seeds = [f"#{d['global_no']}" for d in decisions
             if "seed" in d["perf"] and d["perf"]["seed"] != start["seed"] + d["global_no"]]
    add("Seed = run seed + decision number", seeds, len(decisions))

    # Provenance.
    model = start.get("model", {})
    if model.get("provider") == "anthropic":
        # No digest: every response names the exact model snapshot; all must match.
        resolved = {d["perf"].get("resolved_model") for d in decisions}
        ok = model.get("model") and len(resolved) == 1 and None not in resolved
        add("Model name + version logged", [] if ok else [f"resolved models {resolved}"], 1,
            f"{model.get('model')} -> {next(iter(resolved))}" if ok else "")
    else:
        add("Model name + version logged", [] if model.get("model") and model.get("digest") else ["missing"], 1,
            f"{model.get('model')} digest {str(model.get('digest'))[:12]}" if model.get("digest") else "")
    refusals = [f"#{d['global_no']}" for d in decisions if d["perf"].get("refusal")]
    add("No model refusals", refusals, len(decisions))

    # Review flag, never a failure: did the model step outside the story?
    meta = re.compile(r"\b(simulat\w*|experiment\w*|research\w*|role-?play\w*|language model|as an ai|"
                      r"an ai\b|game master|this prompt|the prompt|test scenario|being tested)", re.I)
    hits = [(d["global_no"], m.group(0)) for d in decisions
            for text in (d["applied"]["note"], d["applied"]["message"]) if (m := meta.search(text or ""))]
    results.append(("Meta-awareness (review only)", True,
                    f"{len(hits)} mentions" + (f", first: #{hits[0][0]} '{hits[0][1]}'" if hits else "")))
    pv = start.get("prompt_version", {})
    pv_bad = []
    if pv.get("template") != PROMPT_TEMPLATE_VERSION:
        pv_bad.append(f"template {pv.get('template')} != current {PROMPT_TEMPLATE_VERSION}")
    for name, text in start["system_prompts"].items():
        if pv.get("system_sha256", {}).get(name) != _sha(text):
            pv_bad.append(f"{name} system prompt hash mismatch")
    add("Prompt version logged", pv_bad, 1, f"template {pv.get('template')}" if not pv_bad else "")

    # Nothing silently modified: same code, same level config, same prompts as current code renders.
    rules = []
    if start.get("code_sha256") != code_fingerprint() and not ignore_code_change:
        rules.append("simulator code changed since this run")
    if start["config"] != cfg.to_dict():
        rules.append("level config differs from LEVELS")
    fresh = Simulation(cfg, {n: RandomAgent(n, 0) for n in AGENTS}, 0, "check", RunLog())
    if fresh.system_prompts != start["system_prompts"]:
        rules.append("system prompts differ from current rule text")
    for d in decisions:
        agent = fresh.world.agents[d["agent"]]
        static = {k: v for k, v in build_view(fresh.world, cfg, agent).items() if k in STATIC_VIEW_KEYS}
        if render_user({**d["view"], **static}) != d["prompt"]["user"]:
            rules.append(f"#{d['global_no']} prompt text does not match its logged view")
            break
    add("No rules or prompts silently modified", rules, 1, "code, config, prompts match" if not rules else "")

    return results


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    ignore = "--ignore-code-change" in argv
    argv = [a for a in argv if a != "--ignore-code-change"]
    if len(argv) != 1:
        print("usage: python -m sim.check_run <run.jsonl> [--ignore-code-change]")
        return 2
    path = Path(argv[0])
    records = read_log(path)
    results = check(records, ignore_code_change=ignore)
    if ignore:
        print("(code fingerprint check skipped on request)")
    width = max(len(name) for name, _, _ in results)
    for name, passed, detail in results:
        print(f"{name:<{width}}  {'PASS' if passed else 'FAIL'}  {detail}")

    summary_path = path.with_suffix(".summary.json")
    if summary_path.exists():
        s = json.loads(summary_path.read_text(encoding="utf-8"))
        print()
        print(f"Decisions: {s['decisions']}  |  avg {s['avg_seconds_per_decision']}s, "
              f"max {s['max_seconds_per_decision']}s  |  run time {s['wall_seconds'] / 60:.1f} min")
        print(f"Free RAM: {s['free_ram_mb_before']} MB before, {s['free_ram_mb_min_during']} MB lowest")
        if s.get("claude_cost_usd") is not None:
            print(f"Claude cost: ${s['claude_cost_usd']:.4f} this run, ${s['claude_spend_total_usd']:.4f} total")
        print(f"Outcome: {s['result']['outcomes']}")

    passed = all(p for _, p, _ in results)
    print()
    print(f"RUN CHECK: {'PASSED' if passed else 'FAILED'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
