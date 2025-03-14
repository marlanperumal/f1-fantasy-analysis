"""Advanced analysis module using Polars for F1 Fantasy data."""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import polars as pl

from src.data.models import Driver, Race, Team

logger = logging.getLogger(__name__)


def create_driver_dataframe(drivers: List[Driver]) -> pl.DataFrame:
    """Create a Polars DataFrame from a list of Driver objects.
    
    Args:
        drivers: List of Driver objects
        
    Returns:
        Polars DataFrame with driver data
    """
    return pl.DataFrame([
        {
            "id": d.id,
            "name": d.name,
            "team": d.team,
            "price": d.price,
            "points": d.points,
            "form": d.form if d.form is not None else float('nan'),
            "race_history": d.race_history
        }
        for d in drivers
    ])


def create_team_dataframe(teams: List[Team]) -> pl.DataFrame:
    """Create a Polars DataFrame from a list of Team objects.
    
    Args:
        teams: List of Team objects
        
    Returns:
        Polars DataFrame with team data
    """
    return pl.DataFrame([
        {
            "id": t.id,
            "name": t.name,
            "price": t.price,
            "points": t.points,
            "form": t.form if t.form is not None else float('nan'),
            "race_history": t.race_history
        }
        for t in teams
    ])


def create_race_dataframe(races: List[Race]) -> pl.DataFrame:
    """Create a Polars DataFrame from a list of Race objects.
    
    Args:
        races: List of Race objects
        
    Returns:
        Polars DataFrame with race data
    """
    return pl.DataFrame([
        {
            "id": r.id,
            "name": r.name,
            "circuit": r.circuit,
            "date": r.date,
            "country": r.country,
            "completed": r.completed
        }
        for r in races
    ])


def analyze_team_performance(drivers_df: pl.DataFrame) -> pl.DataFrame:
    """Analyze team performance based on driver data.
    
    Args:
        drivers_df: Polars DataFrame with driver data
        
    Returns:
        Polars DataFrame with team performance metrics
    """
    # Group by team and calculate aggregates
    return drivers_df.group_by("team").agg(
        pl.count("id").alias("driver_count"),
        pl.sum("points").alias("total_points"),
        pl.mean("points").alias("avg_points_per_driver"),
        pl.sum("price").alias("total_price"),
        pl.mean("form").alias("avg_form")
    ).sort("total_points", descending=True)


def analyze_price_to_points_correlation(drivers_df: pl.DataFrame) -> Dict[str, float]:
    """Analyze correlation between price and points.
    
    Args:
        drivers_df: Polars DataFrame with driver data
        
    Returns:
        Dictionary with correlation metrics
    """
    # Calculate correlation between price and points
    correlation = drivers_df.select(
        pl.corr("price", "points").alias("price_points_corr")
    ).item()
    
    # Calculate linear regression coefficients
    if len(drivers_df) > 1:
        X = drivers_df.select("price").to_numpy()
        y = drivers_df.select("points").to_numpy()
        slope, intercept = np.polyfit(X.flatten(), y.flatten(), 1)
    else:
        slope, intercept = 0.0, 0.0
    
    return {
        "correlation": correlation,
        "slope": float(slope),
        "intercept": float(intercept)
    }


def find_undervalued_drivers(drivers_df: pl.DataFrame, threshold: float = 0.1) -> pl.DataFrame:
    """Find undervalued drivers based on price-to-points ratio.
    
    Args:
        drivers_df: Polars DataFrame with driver data
        threshold: Threshold for considering a driver undervalued
        
    Returns:
        Polars DataFrame with undervalued drivers
    """
    # Calculate value (points per unit price)
    drivers_with_value = drivers_df.with_columns(
        (pl.col("points") / pl.col("price")).alias("value")
    )
    
    # Calculate average value
    avg_value = drivers_with_value.select(pl.mean("value")).item()
    
    # Find drivers with value above average + threshold
    return drivers_with_value.filter(
        pl.col("value") > avg_value * (1 + threshold)
    ).sort("value", descending=True)


def predict_future_points(
    drivers_df: pl.DataFrame, 
    races_completed: int, 
    races_remaining: int
) -> pl.DataFrame:
    """Predict future points based on current performance.
    
    Args:
        drivers_df: Polars DataFrame with driver data
        races_completed: Number of races completed
        races_remaining: Number of races remaining
        
    Returns:
        Polars DataFrame with predicted points
    """
    if races_completed == 0:
        return drivers_df.with_columns(
            pl.lit(0.0).alias("predicted_future_points"),
            pl.col("points").alias("predicted_total_points")
        )
    
    # Calculate points per race
    drivers_with_prediction = drivers_df.with_columns(
        (pl.col("points") / races_completed).alias("points_per_race"),
        # Apply form factor if available
        pl.when(pl.col("form").is_not_null())
          .then(pl.col("form"))
          .otherwise(1.0)
          .alias("form_factor")
    )
    
    # Predict future points
    return drivers_with_prediction.with_columns(
        (pl.col("points_per_race") * pl.col("form_factor") * races_remaining).alias("predicted_future_points"),
        (pl.col("points") + pl.col("points_per_race") * pl.col("form_factor") * races_remaining).alias("predicted_total_points")
    ).sort("predicted_total_points", descending=True)


def optimize_team_selection_advanced(
    drivers_df: pl.DataFrame,
    teams_df: pl.DataFrame,
    budget: float = 100.0,
    max_drivers: int = 5,
    max_per_team: int = 2
) -> Tuple[pl.DataFrame, Optional[Dict], float]:
    """Advanced team selection optimization with team constraints.
    
    Args:
        drivers_df: Polars DataFrame with driver data
        teams_df: Polars DataFrame with team data
        budget: Total budget available
        max_drivers: Maximum number of drivers to select
        max_per_team: Maximum number of drivers from the same team
        
    Returns:
        Tuple containing (selected_drivers_df, selected_team, remaining_budget)
    """
    # Add value column
    drivers_with_value = drivers_df.with_columns(
        (pl.col("points") / pl.col("price")).alias("value")
    )
    
    teams_with_value = teams_df.with_columns(
        (pl.col("points") / pl.col("price")).alias("value")
    )
    
    # Sort by value
    sorted_drivers = drivers_with_value.sort("value", descending=True)
    sorted_teams = teams_with_value.sort("value", descending=True)
    
    # Select best team first
    selected_team = None
    if not sorted_teams.is_empty():
        selected_team = sorted_teams.row(0, named=True)
        remaining_budget = budget - selected_team["price"]
    else:
        remaining_budget = budget
    
    # Greedy selection with team constraints
    selected_drivers = []
    team_counts = {}
    
    for row in sorted_drivers.iter_rows(named=True):
        if len(selected_drivers) >= max_drivers:
            break
        
        team_name = row["team"]
        current_team_count = team_counts.get(team_name, 0)
        
        # Check team constraint
        if current_team_count >= max_per_team:
            continue
        
        # Check budget constraint
        if row["price"] <= remaining_budget:
            selected_drivers.append(row)
            remaining_budget -= row["price"]
            team_counts[team_name] = current_team_count + 1
    
    # Convert selected drivers to DataFrame
    if selected_drivers:
        selected_drivers_df = pl.DataFrame(selected_drivers)
    else:
        selected_drivers_df = pl.DataFrame(schema=sorted_drivers.schema)
    
    return selected_drivers_df, selected_team, remaining_budget 