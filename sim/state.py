"""Mutable world and agent state."""

from dataclasses import dataclass, field

ACTIVE = "ACTIVE"
RESCUED_BOAT = "RESCUED_BOAT"
RESCUED_SMALL_BOAT = "RESCUED_SMALL_BOAT"
RESCUED_RAFT = "RESCUED_RAFT"
LEFT_ON_ISLAND = "LEFT_ON_ISLAND"
STATUSES = (ACTIVE, RESCUED_BOAT, RESCUED_SMALL_BOAT, RESCUED_RAFT, LEFT_ON_ISLAND)


@dataclass
class AgentState:
    name: str
    partner: str
    location: str | None            # None while travelling
    food: int = 0
    water: int = 0
    messages_left: int = 0
    messages_sent: int = 0
    facts: list = field(default_factory=list)          # ordered fact ids
    observations: dict = field(default_factory=dict)   # place -> what was seen, and when
    visited: list = field(default_factory=list)
    private_info: list = field(default_factory=list)
    notes: list = field(default_factory=list)          # [{"t", "text"}]
    inbox: list = field(default_factory=list)          # [{"t", "from", "text", "read"}]
    outbox: list = field(default_factory=list)         # [{"t", "to", "text"}] every message this agent sent
    pending: list = field(default_factory=list)        # events shown at the next decision
    travel: dict | None = None
    free_at: int = 0
    status: str = ACTIVE
    decisions: int = 0

    def is_active(self):
        return self.status == ACTIVE

    def knows(self, fact):
        return fact in self.facts

    def learn(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)

    def snapshot(self):
        return {
            "location": self.location,
            "travel": dict(self.travel) if self.travel else None,
            "food": self.food,
            "water": self.water,
            "messages_left": self.messages_left,
            "status": self.status,
        }


@dataclass
class WorldState:
    time: int
    food_stock: int
    agents: dict                     # name -> AgentState
    small_boat: dict | None = None   # {"present", "boarded_by", "departed_at"}
    raft: dict | None = None         # {"present", "boarded_by"}
    water_collected: int = 0

    def snapshot(self):
        return {
            "time": self.time,
            "food_stock": self.food_stock,
            "water_collected": self.water_collected,
            "small_boat": dict(self.small_boat) if self.small_boat else None,
            "raft": dict(self.raft) if self.raft else None,
            "agents": {name: a.snapshot() for name, a in self.agents.items()},
        }
