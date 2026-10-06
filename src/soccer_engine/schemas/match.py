from typing import Any
from pydantic import BaseModel, Field

class TeamSnapshot(BaseModel):
    name: str
    elo: float = 1500
    pi: float = 0
    attack: float = 1.0
    defense: float = 1.0
    home_strength: float = 0
    away_strength: float = 0
    form_points: float = 0.5
    xg_for: float = 1.35
    xg_against: float = 1.35
    goals_for: float = 1.35
    goals_against: float = 1.35

class ContextSnapshot(BaseModel):
    home_advantage: float = 0.15
    lineup_certainty: float = Field(1.0, ge=0, le=1)
    data_quality: float = Field(1.0, ge=0, le=1)
    weather_impact: float = 0
    travel_impact: float = 0
    referee_impact: float = 0

class MarketSnapshot(BaseModel):
    home_odds: float | None = None
    draw_odds: float | None = None
    away_odds: float | None = None

class MatchRequest(BaseModel):
    match_id: str = "demo"
    home: TeamSnapshot
    away: TeamSnapshot
    context: ContextSnapshot = ContextSnapshot()
    market: MarketSnapshot = MarketSnapshot()
    metadata: dict[str, Any] = {}
