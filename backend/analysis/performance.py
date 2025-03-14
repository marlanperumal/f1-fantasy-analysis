"""Performance analysis module for F1 Fantasy data."""

import logging
from typing import Dict, List, Tuple

import numpy as np
import polars as pl

from backend.data.models import Driver, Team

logger = logging.getLogger(__name__)


def calculate_value_efficiency(driver: Driver) -> float:
    """Calculate the points per million spent for a driver.

    Args:
        driver: Driver object

    Returns:
        Points per million spent
    """
    if driver.price <= 0:
        return 0.0
    
    return driver.points / driver.price


def calculate_team_value_efficiency(team: Team) -> float:
    """Calculate the points per million spent for a team.

    Args:
        team: Team object

    Returns:
        Points per million spent
    """
    if team.price <= 0:
        return 0.0
    
    return team.points / team.price


def rank_drivers_by_value(drivers: List[Driver]) -> List[Tuple[Driver, float]]:
    """Rank drivers by value efficiency (points per million).

    Args:
        drivers: List of Driver objects

    Returns:
        List of tuples containing (Driver, value_efficiency) sorted by value efficiency
    """
    driver_values = [(driver, calculate_value_efficiency(driver)) for driver in drivers]
    return sorted(driver_values, key=lambda x: x[1], reverse=True)


def rank_teams_by_value(teams: List[Team]) -> List[Tuple[Team, float]]:
    """Rank teams by value efficiency (points per million).

    Args:
        teams: List of Team objects

    Returns:
        List of tuples containing (Team, value_efficiency) sorted by value efficiency
    """
    team_values = [(team, calculate_team_value_efficiency(team)) for team in teams]
    return sorted(team_values, key=lambda x: x[1], reverse=True)


def analyze_form_trends(drivers: List[Driver]) -> Dict[str, float]:
    """Analyze recent form trends for drivers.

    Args:
        drivers: List of Driver objects

    Returns:
        Dictionary mapping driver names to their form trend (last 3 races)
    """
    trends = {}
    
    for driver in drivers:
        # Get the last 3 races if available
        recent_races = driver.race_history[-3:] if len(driver.race_history) >= 3 else driver.race_history
        
        if recent_races:
            # Calculate the trend (positive or negative)
            if len(recent_races) >= 2:
                # Simple linear regression slope
                x = np.arange(len(recent_races))
                slope, _ = np.polyfit(x, recent_races, 1)
                trends[driver.name] = slope
            else:
                trends[driver.name] = 0.0
        else:
            trends[driver.name] = 0.0
    
    return trends


def optimal_team_selection(
    drivers: List[Driver], teams: List[Team], budget: float = 100.0, max_drivers: int = 5
) -> Tuple[List[Driver], Team, float]:
    """Select the optimal team based on value efficiency within budget constraints.

    Args:
        drivers: List of Driver objects
        teams: List of Team objects
        budget: Total budget available
        max_drivers: Maximum number of drivers to select

    Returns:
        Tuple containing (selected_drivers, selected_team, remaining_budget)
    """
    # Convert to Polars DataFrames for more efficient processing
    driver_data = pl.DataFrame([
        {
            "id": d.id,
            "name": d.name,
            "price": d.price,
            "points": d.points,
            "value": calculate_value_efficiency(d)
        }
        for d in drivers
    ])
    
    team_data = pl.DataFrame([
        {
            "id": t.id,
            "name": t.name,
            "price": t.price,
            "points": t.points,
            "value": calculate_team_value_efficiency(t)
        }
        for t in teams
    ])
    
    # Sort by value efficiency
    driver_data = driver_data.sort("value", descending=True)
    team_data = team_data.sort("value", descending=True)
    
    # Start with the best team
    selected_team = next((t for t in teams if t.id == team_data[0, "id"]), None) if not team_data.is_empty() else None
    remaining_budget = budget - (selected_team.price if selected_team else 0)
    
    # Select drivers greedily by value within budget
    selected_drivers = []
    for row in driver_data.iter_rows(named=True):
        if len(selected_drivers) >= max_drivers:
            break
            
        driver_id = row["id"]
        driver_price = row["price"]
        
        if driver_price <= remaining_budget:
            driver = next((d for d in drivers if d.id == driver_id), None)
            if driver:
                selected_drivers.append(driver)
                remaining_budget -= driver_price
    
    return selected_drivers, selected_team, remaining_budget 