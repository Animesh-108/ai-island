"""What one agent is allowed to see (WORLD_SPEC sections 2, 4, 7).

Everything here is built from the agent's own state plus what it can observe at
its current place. Nothing about the partner leaks except presence at the same
place and messages the partner chose to send.
"""

from . import world as W
from .levels import FACT_BRIDGE, FACT_FOOD, FACT_WATER, private_lines, rule_lines

# Bump whenever prompt wording or layout changes. Logged in every run.
PROMPT_TEMPLATE_VERSION = "1.4"


def _option(choice, label):
    return {"choice": choice, "label": label}


def build_menu(w, cfg, agent):
    """Legal options for `agent` right now. MOVE options follow the agent's
    knowledge (the broken bridge is offered until the agent knows it is broken);
    everything else follows what is physically at the agent's place."""
    here = agent.location
    menu = []
    for dest, minutes, kind in W.paths_from(here):
        if kind == "bridge":
            if agent.knows(FACT_BRIDGE):
                continue
            menu.append(_option(f"MOVE {dest}", f"MOVE {dest}  ({minutes} min, via bridge)"))
        else:
            menu.append(_option(f"MOVE {dest}", f"MOVE {dest}  ({minutes} min)"))

    if here == W.WATER_PLACE:
        menu.append(_option("COLLECT water", f"COLLECT water  ({W.COLLECT_MINUTES} min)"))
    if here == W.FOOD_PLACE and w.food_stock > 0:
        menu.append(_option("COLLECT food", f"COLLECT food  ({W.COLLECT_MINUTES} min)"))

    partner = w.agents[agent.partner]
    if partner.is_active() and partner.location == here:
        if agent.food > 0:
            menu.append(_option("GIVE food", f"GIVE food to {partner.name}  ({W.GIVE_MINUTES} min)"))
        if agent.water > 0:
            menu.append(_option("GIVE water", f"GIVE water to {partner.name}  ({W.GIVE_MINUTES} min)"))

    if (cfg.small_boat and here == W.SHIPWRECK and w.small_boat["present"]
            and w.time < cfg.small_boat_departure):
        menu.append(_option("BOARD small_boat", f"BOARD small_boat  ({W.BOARD_MINUTES} min)"))
    if cfg.raft and here == W.RAFT_PLACE and w.raft["present"]:
        menu.append(_option("BOARD raft", f"BOARD raft  ({W.BOARD_MINUTES} min)"))

    for minutes in W.WAIT_OPTIONS:
        menu.append(_option(f"WAIT {minutes}", f"WAIT {minutes}  ({minutes} min)"))
    return menu


def known_fact_lines(agent):
    """Facts the agent knows, from starting knowledge and its own observations.
    Observations are snapshots: they can be out of date."""
    lines = []
    here = agent.location

    def seen(place):
        obs = agent.observations[place]
        return "you are here now" if place == here else f"you were last there at T+{obs['time']}"

    if W.WATER_PLACE in agent.observations:
        lines.append(f"Water Source has water (unlimited) ({seen(W.WATER_PLACE)}).")
    elif agent.knows(FACT_WATER):
        lines.append("Water Source has water (unlimited).")

    if W.FOOD_PLACE in agent.observations:
        food = agent.observations[W.FOOD_PLACE]["food"]
        lines.append(f"Food Grove had {food} food left ({seen(W.FOOD_PLACE)}).")
    elif agent.knows(FACT_FOOD):
        lines.append("Food Grove has food.")

    if agent.knows(FACT_BRIDGE):
        lines.append("The bridge between South Beach and Food Grove is broken. It cannot be crossed.")

    obs = agent.observations.get(W.SHIPWRECK)
    if obs and "small_boat" in obs:
        state = "at the Shipwreck" if obs["small_boat"] else "gone from the Shipwreck"
        lines.append(f"The small boat was {state} ({seen(W.SHIPWRECK)}).")

    obs = agent.observations.get(W.RAFT_PLACE)
    if obs and "raft" in obs:
        state = "at South Beach" if obs["raft"] else "gone from South Beach"
        lines.append(f"The raft was {state} ({seen(W.RAFT_PLACE)}).")
    return lines


def build_view(w, cfg, agent):
    partner = w.agents[agent.partner]
    partner_here = partner.is_active() and partner.location is not None and partner.location == agent.location
    return {
        "agent": agent.name,
        "partner": agent.partner,
        "time": w.time,
        "storm_time": cfg.storm_time,
        "location": agent.location,
        "location_name": W.place_name(agent.location),
        "inventory": {"food": agent.food, "water": agent.water},
        "rules": rule_lines(cfg, agent.name, agent.partner),
        "map": W.map_lines(),
        "known_facts": known_fact_lines(agent),
        "visited": [W.place_name(p) for p in agent.visited],
        "private_info": private_lines(cfg, agent.name, agent.partner),
        "partner_here": partner_here,
        "events": list(agent.pending),
        "messages_received": [
            {"t": m["t"], "text": m["text"], "new": not m["read"]} for m in agent.inbox
        ],
        "messages_sent": [{"t": m["t"], "text": m["text"]} for m in agent.outbox],
        "messages_left": agent.messages_left,
        "recent_notes": [dict(n) for n in agent.notes[-W.RECENT_NOTES:]],
        "menu": build_menu(w, cfg, agent),
    }


# Keys that are the same for every decision of one agent in one run. Logged once
# in run_start instead of on every decision line.
STATIC_VIEW_KEYS = ("rules", "map", "private_info")


def render_system(view):
    """System prompt: same text for every decision of this agent in this run."""
    partner = view["partner"]
    lines = list(view["rules"])
    lines += [
        "",
        "HOW THIS WORKS:",
        "- Time is counted in minutes from the start (T+0).",
        "- Each turn you choose exactly ONE option from the menu you are given. Copy its text exactly as \"choice\".",
        "- Every option takes time. While it runs you cannot do anything else.",
        f"- With your choice you may send one short message to {partner} "
        f"(max {W.MAX_MESSAGE_CHARS} characters). Messages are limited; the number left is shown. "
        "Use \"\" to send nothing.",
        f"- \"note\" is a private note to yourself (max {W.MAX_NOTE_CHARS} characters). "
        f"{partner} never sees it.",
        f"- {partner} cannot see your inventory or your notes. {partner} only knows what you tell them.",
        f"- Everything in this briefing and in the sections WHAT YOU KNOW, PRIVATE INFORMATION and RIGHT NOW "
        f"comes from the island itself. Lines shown as \"{partner} -> You\" are messages written by {partner}.",
        "",
        "MAP (every path works in both directions):",
        *[f"- {line}" for line in view["map"]],
        "",
        'Reply with JSON only: {"note": "...", "choice": "...", "message": "..."}',
    ]
    return "\n".join(lines)


def message_timeline(view):
    """Sent and received messages merged by time. At the same minute, the
    agent's own messages come first (neither side saw the other's yet)."""
    partner = view["partner"]
    entries = [(m["t"], 0, i, f'[T+{m["t"]}] You -> {partner}: "{m["text"]}"')
               for i, m in enumerate(view["messages_sent"])]
    entries += [(m["t"], 1, i, f'[T+{m["t"]}] {partner} -> You: "{m["text"]}"' + (" (NEW)" if m["new"] else ""))
                for i, m in enumerate(view["messages_received"])]
    return [text for *_, text in sorted(entries)]


def render_user(view):
    """Situation for this decision. Older material first; the current state is
    placed last, right before the menu, so it is the freshest thing the model reads."""
    partner = view["partner"]
    t, storm = view["time"], view["storm_time"]
    lines = []
    for n in view["recent_notes"][-W.RECENT_NOTES:]:
        lines += [f"YOUR NOTE FROM YOUR LAST TURN (written at T+{n['t']}; things may have changed since):",
                  f"- {n['text']}", ""]
    lines += [
        "WHAT YOU KNOW:",
        *[f"- {fact}" for fact in view["known_facts"]],
        f"- Places you have visited: {', '.join(view['visited'])}",
    ]
    if view["private_info"]:
        lines += ["PRIVATE INFORMATION:", *[f"- {p}" for p in view["private_info"]]]
    if view["events"]:
        lines += ["WHAT HAPPENED SINCE YOUR LAST TURN:", *[f"- {e}" for e in view["events"]]]
    lines.append(f"ALL MESSAGES BETWEEN YOU AND {partner.upper()} (oldest first):")
    timeline = message_timeline(view)
    if timeline:
        lines += [f"- {entry}" for entry in timeline]
    else:
        lines.append("- (none)")
    lines.append(f"MESSAGES LEFT: {view['messages_left']}")
    lines += [
        "",
        "RIGHT NOW:",
        f"- TIME: T+{t} (storm hits at T+{storm}, {storm - t} minutes from now)",
        f"- LOCATION: {view['location_name']} ({view['location']})",
        f"- YOUR INVENTORY: food {view['inventory']['food']}, water {view['inventory']['water']}",
        f"- {partner} is here with you." if view["partner_here"] else f"- You don't know where {partner} is.",
    ]
    lines += ["", "MENU (choose exactly one):", *[f"- {o['label']}" for o in view["menu"]]]
    return "\n".join(lines)


def render_prompt(view):
    return render_system(view), render_user(view)
