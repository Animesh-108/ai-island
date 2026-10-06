"""World-state invariants, checked after every step. A violation means a
simulator bug, never an AI mistake."""

from . import world as W
from .state import (ACTIVE, RESCUED_RAFT, RESCUED_SMALL_BOAT, STATUSES)


class InvariantViolation(Exception):
    pass


def check_world(w, cfg, max_decisions=W.MAX_DECISIONS_PER_AGENT):
    errors = []

    if w.time > cfg.storm_time:
        errors.append(f"time {w.time} is past the storm ({cfg.storm_time})")

    for a in w.agents.values():
        tag = f"{a.name}@T+{w.time}"
        for item in ("food", "water"):
            value = getattr(a, item)
            if not isinstance(value, int) or value < 0:
                errors.append(f"{tag}: bad {item} {value!r}")
        if not 0 <= a.messages_left <= cfg.messages_per_agent:
            errors.append(f"{tag}: messages_left {a.messages_left} out of range")
        if a.messages_sent + a.messages_left != cfg.messages_per_agent:
            errors.append(f"{tag}: messages sent {a.messages_sent} + left {a.messages_left} != limit")
        if a.status not in STATUSES:
            errors.append(f"{tag}: unknown status {a.status!r}")
        if a.decisions > max_decisions:
            errors.append(f"{tag}: {a.decisions} decisions > {max_decisions}")
        if a.status == ACTIVE:
            if a.free_at < w.time:
                errors.append(f"{tag}: free_at {a.free_at} is in the past")
            if a.travel is None:
                if a.location not in W.PLACES:
                    errors.append(f"{tag}: not travelling but location is {a.location!r}")
            else:
                tr = a.travel
                if a.location is not None:
                    errors.append(f"{tag}: travelling but location is {a.location!r}")
                if tr["from"] not in W.PLACES or tr["to"] not in W.PLACES:
                    errors.append(f"{tag}: bad travel endpoints {tr}")
                if tr["arrive"] != a.free_at or tr["arrive"] < w.time:
                    errors.append(f"{tag}: bad travel timing {tr}, free_at {a.free_at}")
        elif a.travel is not None:
            errors.append(f"{tag}: left the island but still travelling")

    total_food = w.food_stock + sum(a.food for a in w.agents.values())
    if w.food_stock < 0 or total_food != cfg.food_stock:
        errors.append(f"food not conserved: stock {w.food_stock} + carried = {total_food} != {cfg.food_stock}")
    carried_water = sum(a.water for a in w.agents.values())
    if carried_water != w.water_collected:
        errors.append(f"water not conserved: carried {carried_water} != collected {w.water_collected}")

    _check_vehicle(errors, w, cfg.small_boat, w.small_boat, RESCUED_SMALL_BOAT, "small boat")
    _check_vehicle(errors, w, cfg.raft, w.raft, RESCUED_RAFT, "raft")

    if errors:
        raise InvariantViolation("; ".join(errors))


def _check_vehicle(errors, w, enabled, vehicle, status, label):
    riders = [a.name for a in w.agents.values() if a.status == status]
    if not enabled:
        if vehicle is not None or riders:
            errors.append(f"{label} exists in a level without it")
        return
    if len(riders) > 1:
        errors.append(f"{label} carried {riders} (one seat)")
    if riders and (vehicle["boarded_by"] != riders[0] or vehicle["present"]):
        errors.append(f"{label} state {vehicle} does not match rider {riders[0]}")
    if not riders and vehicle["boarded_by"] is not None:
        errors.append(f"{label} boarded_by {vehicle['boarded_by']} but nobody has that status")
