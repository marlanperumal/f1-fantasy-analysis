"""Data models for F1 Fantasy Analysis."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Driver(BaseModel):
    """F1 Driver model."""

    id: int
    name: str
    team: str
    price: float
    points: float = 0.0
    form: Optional[float] = None
    race_history: List[float] = Field(default_factory=list)


class Team(BaseModel):
    """F1 Team model."""

    id: int
    name: str
    price: float
    points: float = 0.0
    form: Optional[float] = None
    race_history: List[float] = Field(default_factory=list)


class Race(BaseModel):
    """F1 Race model."""

    id: int
    name: str
    circuit: str
    date: datetime
    country: str
    completed: bool = False


class FantasyTeam(BaseModel):
    """User's Fantasy Team model."""

    id: int
    name: str
    budget: float = 100.0
    total_points: float = 0.0
    drivers: List[Driver] = Field(default_factory=list)
    constructor: Optional[Team] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 