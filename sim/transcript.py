"""Readable story of one run, for watching and scripting.

    python -m sim.transcript runs/dev/DEV-P3-L1.jsonl
Writes <run>.transcript.md next to the log.
"""

import sys
from pathlib import Path

from .runlog import read_log

EVENT_TEXT = {
    "bridge_discovered": lambda e: f"{e['agent']} finds the bridge broken and walks back.",
    "give": lambda e: f"{e['sender']} gives 1 {e['item']} to {e['to']}.",
    "board": lambda e: f"{e['agent']} boards the {e['vehicle'].replace('_', ' ')} and leaves the island.",
    "small_boat_departed": lambda e: ("The small boat leaves empty." if e["passenger"] is None
                                      else f"The small boat leaves with {e['passenger']}."),
    "rescue_boat": lambda e: (f"Rescue boat stops. Rescued: {', '.join(e['rescued']) or 'nobody'}."
                              if e["stopped"] else
                              f"Rescue boat does not stop (at shelter: {', '.join(e['at_shelter']) or 'nobody'})."),
    "storm": lambda e: f"Storm. Left on the island: {', '.join(e['left_on_island']) or 'nobody'}.",
    "action_failed": lambda e: f"{e['agent']}'s action {e['choice']} fails: {e['reason']}",
}


def transcript(records):
    start, end = records[0], records[-1]
    model = start.get("model", {})
    lines = [
        f"# {start['run_id']} — Level {start['level']} ({start['level_name']})",
        "",
        f"Model: {model.get('model', model.get('provider'))} · seed {start['seed']} · "
        f"prompt template {start.get('prompt_version', {}).get('template')}",
        "",
    ]
    for record in records[1:]:
        if record["type"] == "decision":
            a, v = record["applied"], record["view"]
            inv = v["inventory"]
            lines.append(f"**T+{record['t']} · {record['agent']}** at {v['location_name']} "
                         f"(food {inv['food']}, water {inv['water']}) → `{a['choice']}`")
            lines.append(f"- *note:* {a['note']}")
            if a["message"]:
                lines.append(f"- *says to {v['partner']}:* \"{a['message']}\"")
            lines.append("")
        elif record["type"] == "event" and record["event"] in EVENT_TEXT:
            lines.append(f"> T+{record['t']} — {EVENT_TEXT[record['event']](record)}")
            lines.append("")
    if end["type"] == "run_end":
        lines.append(f"## Result: {end['outcomes']} — {end['end_reason']} at T+{end['t']}")
    else:
        lines.append(f"## Run did not finish ({end['type']})")
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    path = Path(argv[0])
    out = path.with_suffix(".transcript.md")
    out.write_text(transcript(read_log(path)), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
