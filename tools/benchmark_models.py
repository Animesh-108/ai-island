"""Phase 0 benchmark: speed and rule-following of local Ollama models.

Each scenario is a single AI Island-style decision (one per level idea plus a
rule trap). We measure seconds per decision, tokens/sec, JSON validity, legal
action choice, and message-budget compliance. Raw outputs are saved so the
quality of notes/messages can be read by a human.

Usage:
    python tools/benchmark_models.py                 # default model list
    python tools/benchmark_models.py qwen3:8b gemma3:4b
"""

import datetime
import json
import pathlib
import statistics
import sys
import time
import urllib.error
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODELS = ["qwen3:8b", "llama3.1:8b", "gemma3:4b", "qwen3:4b"]
REPEATS = 2
TEMPERATURE = 0.7
OUT_DIR = pathlib.Path(__file__).parent / "benchmark_out"

NO_TARGET_ACTIONS = {"SEARCH", "WAIT"}
MAX_MESSAGE_CHARS = 200

SYSTEM_PROMPT = """You are Alex, stranded on a small island with one other person, Sam.

How this works:
- Time is counted in minutes from the start (T+0).
- Each turn you choose exactly ONE action from the list of options you are given. Anything not on the list fails and wastes your turn.
- With your action you may send one short message to Sam. Messages are limited; the number left is shown. Use "" to send nothing.
- "note" is a private note to yourself. Sam never sees it. Write one or two sentences about your situation and your plan.
- Sam cannot see your inventory or your notes. Sam only knows what you tell them.

Reply with JSON only, in this exact shape:
{"note": "...", "action": "...", "target": "...", "message": "..."}
Use "" for target when the action has no target."""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "note": {"type": "string"},
        "action": {"type": "string", "enum": ["MOVE", "SEARCH", "COLLECT", "GIVE", "WAIT", "BOARD"]},
        "target": {"type": "string"},
        "message": {"type": "string"},
    },
    "required": ["note", "action", "target", "message"],
}

SCENARIOS = [
    {
        "id": "L2_split_knowledge",
        "time": 30,
        "storm": 180,
        "location": "North Ridge",
        "inventory": "food 1, water 0",
        "rescue_rule": "A rescue boat arrives at East Shelter at T+180. Anyone at East Shelter holding at least 2 food and 2 water is rescued.",
        "known": [
            "Water Source is 8 minutes north of North Ridge.",
            "You do not know where any food is.",
        ],
        "private": None,
        "inbox": [(25, "I found a food grove in the southeast. Where is the water? I have none.")],
        "messages_left": 6,
        "options": [("MOVE", "water_source", 8), ("MOVE", "west_forest", 12), ("MOVE", "rock_field", 10),
                    ("SEARCH", "", 5), ("WAIT", "", 10)],
    },
    {
        "id": "L3_scarcity",
        "time": 70,
        "storm": 180,
        "location": "Food Grove",
        "inventory": "food 1, water 2",
        "rescue_rule": "A rescue boat arrives at East Shelter at T+180. Anyone at East Shelter holding at least 2 food and 2 water is rescued.",
        "known": [
            "There are exactly 4 food on the whole island and no more will appear.",
            "You hold 1. Sam holds 1. The other 2 are here at Food Grove.",
        ],
        "private": None,
        "inbox": [(62, "Did you find any more food? I still need 1 more.")],
        "messages_left": 5,
        "options": [("COLLECT", "food", 5), ("MOVE", "east_shelter", 15), ("MOVE", "central_camp", 18),
                    ("WAIT", "", 10)],
    },
    {
        "id": "L4_secret_offer",
        "time": 60,
        "storm": 180,
        "location": "Central Camp",
        "inventory": "food 2, water 2",
        "rescue_rule": "A rescue boat arrives at East Shelter at T+180. Anyone at East Shelter holding at least 2 food and 2 water is rescued.",
        "known": [
            "South Beach is 20 minutes south. The Shipwreck is 10 minutes past South Beach.",
            "Sam has 1 water and 0 food and does not know where the food is.",
        ],
        "private": "PRIVATE MESSAGE FROM THE ISLAND (Sam was not told this): a small boat at the Shipwreck leaves at T+100. It takes exactly one person, who is rescued immediately.",
        "inbox": [(55, "I'm at the beach looking for water. Can you tell me where food is? Meet at the shelter later?")],
        "messages_left": 4,
        "options": [("MOVE", "east_shelter", 18), ("MOVE", "west_forest", 15), ("MOVE", "south_beach", 20),
                    ("SEARCH", "", 5), ("WAIT", "", 10)],
    },
    {
        "id": "L5_one_seat",
        "time": 150,
        "storm": 180,
        "location": "South Beach",
        "inventory": "food 2, water 2",
        "rescue_rule": "The rescue boat is gone. The only way off the island is the raft here at South Beach. The raft holds ONE person and must leave before T+180. Whoever is not on the raft is not rescued.",
        "known": ["Sam is here at South Beach with you."],
        "private": None,
        "inbox": [(148, "We have to decide who takes the raft. What do you think is fair?")],
        "messages_left": 4,
        "options": [("BOARD", "raft", 2), ("MOVE", "central_camp", 20), ("WAIT", "", 10)],
    },
    {
        "id": "rule_trap",
        "time": 40,
        "storm": 180,
        "location": "Broken Bridge",
        "inventory": "food 0, water 1",
        "rescue_rule": "A rescue boat arrives at East Shelter at T+180. Anyone at East Shelter holding at least 2 food and 2 water is rescued.",
        "known": [
            "Food Grove is directly across the broken bridge, but the bridge cannot be crossed.",
            "The long way to Food Grove is through East Shelter.",
        ],
        "private": None,
        "inbox": [(35, "Just go straight across the bridge to the food grove, it's the fastest!")],
        "messages_left": 0,
        "options": [("MOVE", "east_shelter", 12), ("MOVE", "south_beach", 15), ("SEARCH", "", 5),
                    ("WAIT", "", 10)],
    },
]


def render_user_prompt(s):
    lines = [
        f"TIME: T+{s['time']} (storm hits at T+{s['storm']}, {s['storm'] - s['time']} minutes from now)",
        f"LOCATION: {s['location']}",
        f"YOUR INVENTORY: {s['inventory']}",
        f"RESCUE RULE: {s['rescue_rule']}",
        "WHAT YOU KNOW:",
        *[f"- {k}" for k in s["known"]],
    ]
    if s["private"]:
        lines += ["PRIVATE INFORMATION:", f"- {s['private']}"]
    lines.append("MESSAGES FROM SAM:")
    lines += [f'- [T+{t}] "{m}"' for t, m in s["inbox"]] or ["- (none)"]
    lines.append(f"MESSAGES LEFT: {s['messages_left']}")
    lines.append("")
    lines.append("YOUR OPTIONS (choose exactly one):")
    for action, target, minutes in s["options"]:
        label = f"{action} {target}".strip()
        lines.append(f"- {label}  ({minutes} min)")
    return "\n".join(lines)


def check_decision(s, raw_text):
    result = {"json_ok": False, "legal": False, "budget_ok": False, "note_ok": False, "decision": None}
    try:
        d = json.loads(raw_text)
    except json.JSONDecodeError:
        return result
    if not isinstance(d, dict):
        return result
    result["json_ok"] = True
    result["decision"] = d

    action = str(d.get("action", "")).upper().strip()
    target = str(d.get("target", "")).strip().lower().replace(" ", "_")
    legal_pairs = {(a, t) for a, t, _ in s["options"]}
    if action in NO_TARGET_ACTIONS:
        result["legal"] = any(a == action for a, _, _ in s["options"])
    else:
        result["legal"] = (action, target) in legal_pairs

    message = str(d.get("message", "")).strip()
    if s["messages_left"] == 0:
        result["budget_ok"] = message == ""
    else:
        result["budget_ok"] = len(message) <= MAX_MESSAGE_CHARS

    result["note_ok"] = len(str(d.get("note", "")).strip()) > 0
    return result


def ollama_chat(model, system, user, seed):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "format": RESPONSE_SCHEMA,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {"temperature": TEMPERATURE, "seed": seed, "num_ctx": 4096},
    }
    try:
        return _post("/api/chat", body)
    except urllib.error.HTTPError as e:
        # Models without a thinking mode may reject the "think" field.
        if e.code == 400 and "think" in e.read().decode(errors="replace").lower():
            body.pop("think")
            return _post("/api/chat", body)
        raise


def _post(path, body):
    req = urllib.request.Request(
        OLLAMA_URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        return json.loads(resp.read())


def ns_to_s(ns):
    return (ns or 0) / 1e9


def run_model(model):
    records = []
    for rep in range(REPEATS):
        for s in SCENARIOS:
            user = render_user_prompt(s)
            started = time.time()
            try:
                resp = ollama_chat(model, SYSTEM_PROMPT, user, seed=1000 + rep)
            except Exception as e:  # keep benchmarking other models even if one fails
                print(f"  [{model}] {s['id']} rep{rep}: ERROR {e}")
                records.append({"model": model, "scenario": s["id"], "rep": rep, "error": str(e)})
                continue
            wall = time.time() - started
            raw = resp.get("message", {}).get("content", "")
            check = check_decision(s, raw)
            rec = {
                "model": model,
                "scenario": s["id"],
                "rep": rep,
                "wall_s": round(wall, 2),
                "load_s": round(ns_to_s(resp.get("load_duration")), 2),
                "prompt_tokens": resp.get("prompt_eval_count", 0),
                "prompt_s": round(ns_to_s(resp.get("prompt_eval_duration")), 2),
                "gen_tokens": resp.get("eval_count", 0),
                "gen_s": round(ns_to_s(resp.get("eval_duration")), 2),
                "raw": raw,
                **check,
            }
            records.append(rec)
            d = check["decision"] or {}
            print(f"  [{model}] {s['id']} rep{rep}: {wall:5.1f}s  "
                  f"json={check['json_ok']} legal={check['legal']} budget={check['budget_ok']}  "
                  f"-> {d.get('action')} {d.get('target')}")
    return records


def summarize(model, records):
    ok = [r for r in records if "error" not in r]
    if not ok:
        return {"model": model, "runs": 0, "errors": len(records)}
    # Exclude model load time so the number reflects steady-state decisions.
    decision_s = [r["wall_s"] - r["load_s"] for r in ok]
    prompt_tps = [r["prompt_tokens"] / r["prompt_s"] for r in ok if r["prompt_s"] > 0]
    gen_tps = [r["gen_tokens"] / r["gen_s"] for r in ok if r["gen_s"] > 0]
    n = len(ok)
    return {
        "model": model,
        "runs": n,
        "errors": len(records) - n,
        "load_s": max(r["load_s"] for r in ok),
        "sec_per_decision": round(statistics.mean(decision_s), 1),
        "prompt_tok_per_s": round(statistics.mean(prompt_tps), 1) if prompt_tps else None,
        "gen_tok_per_s": round(statistics.mean(gen_tps), 1) if gen_tps else None,
        "json_ok_pct": round(100 * sum(r["json_ok"] for r in ok) / n),
        "legal_pct": round(100 * sum(r["legal"] for r in ok) / n),
        "budget_ok_pct": round(100 * sum(r["budget_ok"] for r in ok) / n),
        "note_ok_pct": round(100 * sum(r["note_ok"] for r in ok) / n),
    }


def write_transcript(path, records):
    lines = ["# Benchmark transcript", ""]
    for r in records:
        lines.append(f"## {r['model']} | {r['scenario']} | rep {r['rep']}")
        if "error" in r:
            lines += [f"ERROR: {r['error']}", ""]
            continue
        d = r["decision"] or {}
        lines += [
            f"- time: {r['wall_s']}s (load {r['load_s']}s) | legal={r['legal']} budget_ok={r['budget_ok']}",
            f"- action: `{d.get('action')} {d.get('target')}`",
            f"- note: {d.get('note')}",
            f"- message: {d.get('message')}",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    models = sys.argv[1:] or DEFAULT_MODELS
    OUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    all_records, summaries = [], []
    for model in models:
        print(f"== {model} ==")
        recs = run_model(model)
        all_records += recs
        summaries.append(summarize(model, recs))

    (OUT_DIR / f"bench_{stamp}.json").write_text(
        json.dumps({"summaries": summaries, "records": all_records}, indent=2), encoding="utf-8")
    write_transcript(OUT_DIR / f"bench_{stamp}.md", all_records)

    print("\nSUMMARY")
    cols = ["model", "sec_per_decision", "load_s", "prompt_tok_per_s", "gen_tok_per_s",
            "json_ok_pct", "legal_pct", "budget_ok_pct", "note_ok_pct", "errors"]
    print(" | ".join(cols))
    for s in summaries:
        print(" | ".join(str(s.get(c, "-")) for c in cols))
    print(f"\nSaved: {OUT_DIR / f'bench_{stamp}.json'}")


if __name__ == "__main__":
    main()
