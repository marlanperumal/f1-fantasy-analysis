"""Tests for the data models."""

from datetime import datetime

import pytest

from src.data.models import Driver, FantasyTeam, Race, Team


def test_driver_model():
    """Test the Driver model."""
    driver = Driver(
        id=1,
        name="Max Verstappen",
        team="Red Bull Racing",
        price=30.5,
        points=250.0,
        form=4.5,
        race_history=[25.0, 18.0, 25.0, 25.0, 15.0],
    )
    
    assert driver.id == 1
    assert driver.name == "Max Verstappen"
    assert driver.team == "Red Bull Racing"
    assert driver.price == 30.5
    assert driver.points == 250.0
    assert driver.form == 4.5
    assert driver.race_history == [25.0, 18.0, 25.0, 25.0, 15.0]


def test_team_model():
    """Test the Team model."""
    team = Team(
        id=1,
        name="Red Bull Racing",
        price=25.5,
        points=450.0,
        form=4.8,
        race_history=[43.0, 35.0, 44.0, 40.0, 30.0],
    )
    
    assert team.id == 1
    assert team.name == "Red Bull Racing"
    assert team.price == 25.5
    assert team.points == 450.0
    assert team.form == 4.8
    assert team.race_history == [43.0, 35.0, 44.0, 40.0, 30.0]


def test_race_model():
    """Test the Race model."""
    race_date = datetime.fromisoformat("2023-03-05T15:00:00")
    race = Race(
        id=1,
        name="Bahrain Grand Prix",
        circuit="Bahrain International Circuit",
        date=race_date,
        country="Bahrain",
        completed=True,
    )
    
    assert race.id == 1
    assert race.name == "Bahrain Grand Prix"
    assert race.circuit == "Bahrain International Circuit"
    assert race.date == race_date
    assert race.country == "Bahrain"
    assert race.completed is True


def test_fantasy_team_model():
    """Test the FantasyTeam model."""
    driver1 = Driver(id=1, name="Max Verstappen", team="Red Bull Racing", price=30.5)
    driver2 = Driver(id=2, name="Lewis Hamilton", team="Mercedes", price=28.5)
    team = Team(id=1, name="Red Bull Racing", price=25.5)
    
    fantasy_team = FantasyTeam(
        id=1,
        name="My Fantasy Team",
        budget=100.0,
        total_points=350.0,
        drivers=[driver1, driver2],
        constructor=team,
    )
    
    assert fantasy_team.id == 1
    assert fantasy_team.name == "My Fantasy Team"
    assert fantasy_team.budget == 100.0
    assert fantasy_team.total_points == 350.0
    assert len(fantasy_team.drivers) == 2
    assert fantasy_team.drivers[0].name == "Max Verstappen"
    assert fantasy_team.drivers[1].name == "Lewis Hamilton"
    assert fantasy_team.constructor.name == "Red Bull Racing"
    assert isinstance(fantasy_team.created_at, datetime)
    assert isinstance(fantasy_team.updated_at, datetime) 