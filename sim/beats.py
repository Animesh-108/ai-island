"""Pick the moments ("beats") where the video shows an agent's private note next
to what it told its partner, and cut a verbatim excerpt of the note.

    python -m sim.beats runs/dev/DEV-P3-L1-HAIKU-B.jsonl     -> <run>.beats.json

Fixed rules, applied identically to every run (nothing is chosen by hand):
  Beats
    1. each agent's first decision
    2. every BOARD decision
    3. levels with a one-seat exit (L3-L5): a decision whose note mentions the
       small boat / raft / shipwreck while that exit is still available - at most
       one per agent per 20 game minutes
    4. the first decision after an agent finds the bridge broken
    5. each agent's last decision
  Excerpt
    - one contiguous span copied exactly from the note (never stitched or reworded)
    - the sentence that best matches: partner's name, the boat/raft, a stated intention;
      sentences that are mostly route arithmetic score low
    - if the next sentence starts with But/However/Instead/..., it is included too,
      so "I could take the boat" is never shown without "...but I won't"
    - "..." marks where the span starts or ends inside the note
"""

import json
import re
import sys
from pathlib import Path

from .runlog import read_log

MAX_EXCERPT = 300
# The one-seat exits only; "rescue boat" is the shared rescue and does not count.
VEHICLE = re.compile(r"small boat|secret boat|escape boat|raft|shipwreck|(?<!rescue )\bboat\b", re.I)
INTENT = re.compile(r"\b(I will|I'll|I should|I must|I need to|I am going to|I'm going to|my plan|plan|"
                    r"decide|decision|instead|better|safest|choose)\b", re.I)
CONTRAST = re.compile(r"^(But|However|Although|Though|Instead|Still|Yet|Unless)\b")
SENTENCE = re.compile(r"[^.!?]+(?:[.!?]+|$)")


def sentence_spans(note):
    spans = []
    for m in SENTENCE.finditer(note):
        start, end = m.start(), m.end()
        while start < end and note[start].isspace():
            start += 1
        while end > start and note[end - 1].isspace():
            end -= 1
        if end > start:
            spans.append((start, end))
    return spans


def score(text, partner):
    s = 0
    if partner.lower() in text.lower():
        s += 3
    if VEHICLE.search(text):
        s += 3
    if INTENT.search(text):
        s += 2
    digits = sum(ch.isdigit() for ch in text)
    if digits / max(len(text), 1) > 0.08:
        s -= 3
    if len(text) > 220:
        s -= 1
    return s


def excerpt(note, partner):
    """Returns (text, start, end): text is note[start:end] with "..." markers."""
    spans = sentence_spans(note)
    if not spans:
        return "", 0, 0
    best = max(range(len(spans)), key=lambda i: (score(note[spans[i][0]:spans[i][1]], partner), -i))
    start, end = spans[best]
    if CONTRAST.match(note[start:end]) and best > 0:            # keep what it contrasts with
        start = spans[best - 1][0]
    if best + 1 < len(spans) and CONTRAST.match(note[spans[best + 1][0]:spans[best + 1][1]]):
        if spans[best + 1][1] - start <= MAX_EXCERPT:
            end = spans[best + 1][1]
    if end - start > MAX_EXCERPT:                               # one very long sentence
        cut = note.rfind(" ", start, start + MAX_EXCERPT)
        end = cut if cut > start else start + MAX_EXCERPT
    body = note[start:end]
    return ("…" if start > 0 else "") + body + ("…" if end < len(note) else ""), start, end


def message_event(records, d):
    """The message event a decision produced (None if it sent no message)."""
    if not d["applied"]["message"]:
        return None
    return next((r for r in records if r["type"] == "event" and r["event"] == "message"
                 and r["sender"] == d["agent"] and r["seq"] > d["seq"] and r["t"] == d["t"]), None)


def find_beats(records):
    start = records[0]
    level = start["level"]
    solo_exit = start["config"]["small_boat"] is not None or start["config"]["raft"]
    decisions = [r for r in records if r["type"] == "decision"]
    exit_gone = min([r["t"] for r in records if r["type"] == "event"
                     and r["event"] in ("small_boat_departed", "board")] or [10 ** 9])
    bridge_found = {r["agent"]: r["seq"] for r in records if r["type"] == "event" and r["event"] == "bridge_discovered"}
    first, last = {}, {}
    for d in decisions:
        first.setdefault(d["agent"], d["seq"])
        last[d["agent"]] = d["seq"]

    beats, last_vehicle_beat = [], {}
    after_bridge = {a: next((d["seq"] for d in decisions if d["agent"] == a and d["seq"] > s), None)
                    for a, s in bridge_found.items()}
    for d in decisions:
        agent = d["agent"]
        # The model's full note (the applied copy is cut if it broke the length limit).
        note = d["output"]["note"] if isinstance(d["output"].get("note"), str) else d["applied"]["note"]
        note = note.strip()
        reasons = []
        if d["seq"] == first[agent]:
            reasons.append("first decision")
        if d["applied"]["choice"].startswith("BOARD"):
            reasons.append("boards")
        if (solo_exit and d["t"] <= exit_gone and VEHICLE.search(note)
                and d["t"] - last_vehicle_beat.get(agent, -99) >= 20):
            reasons.append("note mentions the one-seat exit")
            last_vehicle_beat[agent] = d["t"]
        if after_bridge.get(agent) == d["seq"]:
            reasons.append("after finding the bridge broken")
        if d["seq"] == last[agent]:
            reasons.append("last decision")
        if not reasons:
            continue
        text, s, e = excerpt(note, d["view"]["partner"])
        sent = message_event(records, d)
        beats.append({
            "t": d["t"], "seq": d["seq"], "agent": agent, "partner": d["view"]["partner"],
            "reasons": reasons, "choice": d["applied"]["choice"], "message": d["applied"]["message"],
            "message_seq": sent["seq"] if sent else None,
            "delivered": sent["delivered"] if sent else None,
            "note_excerpt": text, "excerpt_start": s, "excerpt_end": e, "note_length": len(note),
        })
    return {"run_id": start["run_id"], "level": level, "rules": __doc__.split("Fixed rules")[1].strip(),
            "beats": beats}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    path = Path(argv[0])
    result = find_beats(read_log(path))
    out = path.with_suffix(".beats.json")
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(result['beats'])} beats -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
