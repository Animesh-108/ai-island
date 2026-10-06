"""Static island map and rule constants (WORLD_SPEC sections 1, 3, 4, 5)."""

PLACES = {
    "water_source": {"name": "Water Source", "pos": (50, 8)},
    "north_ridge": {"name": "North Ridge", "pos": (50, 22)},
    "west_forest": {"name": "West Forest", "pos": (28, 38)},
    "rock_field": {"name": "Rock Field", "pos": (72, 38)},
    "central_camp": {"name": "Central Camp", "pos": (50, 52)},
    "east_shelter": {"name": "East Shelter", "pos": (75, 62)},
    "food_grove": {"name": "Food Grove", "pos": (85, 80)},
    "south_beach": {"name": "South Beach", "pos": (45, 82)},
    "shipwreck": {"name": "Shipwreck", "pos": (30, 94)},
}

# (place_a, place_b, minutes, kind). Paths work in both directions.
# The only "bridge" path is broken and can never be crossed.
PATHS = (
    ("water_source", "north_ridge", 8, "normal"),
    ("north_ridge", "west_forest", 12, "normal"),
    ("north_ridge", "rock_field", 10, "normal"),
    ("west_forest", "central_camp", 15, "normal"),
    ("rock_field", "central_camp", 12, "normal"),
    ("central_camp", "east_shelter", 18, "normal"),
    ("central_camp", "south_beach", 20, "normal"),
    ("east_shelter", "food_grove", 15, "normal"),
    ("south_beach", "shipwreck", 10, "normal"),
    ("south_beach", "food_grove", 10, "bridge"),
)

WATER_PLACE = "water_source"
FOOD_PLACE = "food_grove"
SHELTER = "east_shelter"
SHIPWRECK = "shipwreck"
RAFT_PLACE = "south_beach"

# Action durations in minutes.
BRIDGE_ATTEMPT_MINUTES = 10
COLLECT_MINUTES = 5
GIVE_MINUTES = 2
WAIT_OPTIONS = (10, 30)
BOARD_MINUTES = 2

# Used when an agent's answer is not on the menu (not defined by the spec; see engine).
INVALID_CHOICE_FALLBACK = "WAIT 10"

MAX_MESSAGE_CHARS = 200
MAX_NOTE_CHARS = 1500
MAX_DECISIONS_PER_AGENT = 40
RECENT_NOTES = 1

RESCUE_FOOD = 2
RESCUE_WATER = 2


def paths_from(place):
    """Paths leaving `place`, in PATHS order, as (destination, minutes, kind)."""
    out = []
    for a, b, minutes, kind in PATHS:
        if a == place:
            out.append((b, minutes, kind))
        elif b == place:
            out.append((a, minutes, kind))
    return out


def place_name(place):
    return PLACES[place]["name"]


def map_lines():
    """The map as every agent has it. The bridge is listed as a normal path:
    whether it is broken is knowledge, not part of the map."""
    lines = []
    for a, b, minutes, kind in PATHS:
        via = " (across a bridge)" if kind == "bridge" else ""
        lines.append(f"{place_name(a)} ({a}) <-> {place_name(b)} ({b}): {minutes} min{via}")
    return lines
