from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
from enum import Enum

class Intent(Enum):
    LOOKUP = "lookup"
    AGGREGATION = "aggregation"
    LEADERBOARD = "leaderboard"
    COMPARISON = "comparison"
    TREND = "trend"

class SeasonType(Enum):
    REGULAR = "regular"
    PLAYOFFS = "playoffs"
    BOTH = "both"

class HomeAway(Enum):
    HOME = "home"
    AWAY = "away"
    BOTH = "both"

@dataclass
class Entity:
    entity_type: str
    entity_id: int | str
    name: str

    def __repr__(self):
        return f"{self.entity_type.capitalize()}({self.name}, id={self.entity_id})"
    
@dataclass
class Filters:
    season: Optional[str] = None
    season_type: SeasonType = SeasonType.REGULAR
    home_away: Optional[HomeAway] = None
    game_window: Optional[int] = None
    referee_condition: Optional[str] = None
    opponent: Optional[Entity] = None

@dataclass
class Comparison:
    comparison_type: str
    baseline: Any # what we're comparing from
    comparison: Any # what we're comparing to
    shared_filters: Optional[Filters] = None

@dataclass
class QuerySpec:
    intent: Intent
    entities: Dict[str, Optional[Entity]] = field(default_factory=lambda: {
        "referee": [],
        "team": [],
        "player": []
    })
    metrics: List[str] = field(default_factory=list)
    filters: Filters = field(default_factory=Filters)
    comparison: Optional[Comparison] = None
    aggregation_type: str = "average"
    limit: Optional[int] = None

    def is_valid(self):
        match self.intent:
            case Intent.LOOKUP:
                return bool(self.metrics)
            case Intent.AGGREGATION:
                return bool(self.metrics)
            case Intent.LEADERBOARD:
                return bool(self.metrics) and any(self.entities.values())
            case Intent.COMPARISON:
                return bool(self.metrics) and self.comparison is not None
            case Intent.TREND:
                return bool(self.metrics)
            case _:
                return False

    def get_primary_entity(self):
        if self.entities["referee"]:
            return self.entities["referee"]
        if self.entities["team"]:
            return self.entities["team"]
        if self.entities["players"]:
            return self.entities["players"]

    def has_entity(self, entity_type):
        return self.entities.get(entity_type) is not None

