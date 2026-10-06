"""Rebuild world state from a run log's events alone.

Godot and the analysis scripts only read logs. This proves the events carry
enough information: replaying them must reproduce the engine's final state.
"""

import copy

from .state import LEFT_ON_ISLAND, RESCUED_BOAT, RESCUED_RAFT, RESCUED_SMALL_BOAT


def replay(records):
    start = records[0]
    if start["type"] != "run_start":
        raise ValueError("log does not begin with run_start")
    state = copy.deepcopy(start["initial_state"])
    agents = state["agents"]

    for record in records[1:]:
        if record["type"] == "run_end":
            state["time"] = record["t"]
            break
        if record["type"] != "event":
            continue
        state["time"] = record["t"]
        event = record["event"]

        if event == "move_start":
            agent = agents[record["agent"]]
            agent["location"] = None
            agent["travel"] = {k: record[k] for k in ("from", "to", "depart", "arrive", "via_bridge")}
        elif event == "move_end":
            agent = agents[record["agent"]]
            agent["location"] = record["at"]
            agent["travel"] = None
        elif event == "collect":
            agent = agents[record["agent"]]
            agent[record["item"]] += 1
            if record["item"] == "water":
                state["water_collected"] += 1
            else:
                state["food_stock"] -= 1
        elif event == "give":
            agents[record["sender"]][record["item"]] -= 1
            agents[record["to"]][record["item"]] += 1
        elif event == "message":
            agents[record["sender"]]["messages_left"] -= 1
        elif event == "board":
            agent = agents[record["agent"]]
            if record["vehicle"] == "small_boat":
                agent["status"] = RESCUED_SMALL_BOAT
                state["small_boat"].update(present=False, boarded_by=record["agent"], departed_at=record["t"])
            else:
                agent["status"] = RESCUED_RAFT
                state["raft"].update(present=False, boarded_by=record["agent"])
        elif event == "small_boat_departed":
            state["small_boat"]["present"] = False
            state["small_boat"]["departed_at"] = record["t"]
        elif event == "rescue_boat":
            for name in record["rescued"]:
                agents[name]["status"] = RESCUED_BOAT
        elif event == "storm":
            for name in record["left_on_island"]:
                agents[name]["status"] = LEFT_ON_ISLAND
                agents[name]["travel"] = None
        # wait, bridge_discovered, action_failed, simultaneous_order, safety_stop:
        # no change to the replayed state.
    return state
