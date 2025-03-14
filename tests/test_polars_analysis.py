"""Tests for the Polars analysis module."""

import polars as pl
import pytest

from backend.analysis.polars_analysis import (
    analyze_price_to_points_correlation,
    analyze_team_performance,
    create_driver_dataframe,
    create_team_dataframe,
    find_undervalued_drivers,
    optimize_team_selection_advanced,
    predict_future_points,
)
from backend.data.models import Driver, Team


@pytest.fixture
def sample_drivers():
    """Create sample drivers for testing."""
    return [
        Driver(
            id=1,
            name="Max Verstappen",
            team="Red Bull Racing",
            price=30.5,
            points=250.0,
            form=4.5,
            race_history=[25.0, 18.0, 25.0, 25.0, 15.0],
        ),
        Driver(
            id=2,
            name="Lewis Hamilton",
            team="Mercedes",
            price=28.5,
            points=200.0,
            form=3.8,
            race_history=[18.0, 25.0, 15.0, 18.0, 12.0],
        ),
        Driver(
            id=3,
            name="Charles Leclerc",
            team="Ferrari",
            price=26.0,
            points=190.0,
            form=4.0,
            race_history=[15.0, 12.0, 18.0, 15.0, 25.0],
        ),
        Driver(
            id=4,
            name="Sergio Perez",
            team="Red Bull Racing",
            price=24.0,
            points=180.0,
            form=3.5,
            race_history=[12.0, 15.0, 12.0, 10.0, 18.0],
        ),
        Driver(
            id=5,
            name="Carlos Sainz",
            team="Ferrari",
            price=23.0,
            points=170.0,
            form=3.2,
            race_history=[10.0, 10.0, 8.0, 12.0, 10.0],
        ),
    ]


@pytest.fixture
def sample_teams():
    """Create sample teams for testing."""
    return [
        Team(
            id=1,
            name="Red Bull Racing",
            price=35.0,
            points=430.0,
            form=4.0,
            race_history=[37.0, 33.0, 37.0, 35.0, 33.0],
        ),
        Team(
            id=2,
            name="Mercedes",
            price=32.0,
            points=350.0,
            form=3.5,
            race_history=[30.0, 35.0, 25.0, 28.0, 22.0],
        ),
        Team(
            id=3,
            name="Ferrari",
            price=30.0,
            points=360.0,
            form=3.8,
            race_history=[25.0, 22.0, 26.0, 27.0, 35.0],
        ),
    ]


def test_create_driver_dataframe(sample_drivers):
    """Test creating a Polars DataFrame from Driver objects."""
    df = create_driver_dataframe(sample_drivers)
    
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (5, 7)  # 5 rows, 7 columns
    assert df.columns == ["id", "name", "team", "price", "points", "form", "race_history"]
    assert df["name"].to_list() == [
        "Max Verstappen", "Lewis Hamilton", "Charles Leclerc", "Sergio Perez", "Carlos Sainz"
    ]


def test_create_team_dataframe(sample_teams):
    """Test creating a Polars DataFrame from Team objects."""
    df = create_team_dataframe(sample_teams)
    
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (3, 6)  # 3 rows, 6 columns
    assert df.columns == ["id", "name", "price", "points", "form", "race_history"]
    assert df["name"].to_list() == ["Red Bull Racing", "Mercedes", "Ferrari"]


def test_analyze_team_performance(sample_drivers):
    """Test analyzing team performance."""
    drivers_df = create_driver_dataframe(sample_drivers)
    performance_df = analyze_team_performance(drivers_df)
    
    assert isinstance(performance_df, pl.DataFrame)
    assert performance_df.shape == (3, 6)  # 3 teams, 6 metrics
    assert "team" in performance_df.columns
    assert "driver_count" in performance_df.columns
    assert "total_points" in performance_df.columns
    
    # Red Bull Racing should have the highest total points
    assert performance_df[0, "team"] == "Red Bull Racing"
    assert performance_df[0, "driver_count"] == 2
    assert performance_df[0, "total_points"] == 430.0


def test_analyze_price_to_points_correlation(sample_drivers):
    """Test analyzing correlation between price and points."""
    drivers_df = create_driver_dataframe(sample_drivers)
    correlation = analyze_price_to_points_correlation(drivers_df)
    
    assert isinstance(correlation, dict)
    assert "correlation" in correlation
    assert "slope" in correlation
    assert "intercept" in correlation
    assert correlation["correlation"] > 0.9  # Strong positive correlation expected


def test_find_undervalued_drivers(sample_drivers):
    """Test finding undervalued drivers."""
    drivers_df = create_driver_dataframe(sample_drivers)
    undervalued_df = find_undervalued_drivers(drivers_df, threshold=0.0)
    
    assert isinstance(undervalued_df, pl.DataFrame)
    assert "value" in undervalued_df.columns
    
    # At least one driver should be above average value
    assert undervalued_df.shape[0] >= 1


def test_predict_future_points(sample_drivers):
    """Test predicting future points."""
    drivers_df = create_driver_dataframe(sample_drivers)
    prediction_df = predict_future_points(drivers_df, races_completed=5, races_remaining=5)
    
    assert isinstance(prediction_df, pl.DataFrame)
    assert "predicted_future_points" in prediction_df.columns
    assert "predicted_total_points" in prediction_df.columns
    
    # Predicted total points should be greater than current points
    for i in range(len(sample_drivers)):
        assert prediction_df[i, "predicted_total_points"] >= prediction_df[i, "points"]


def test_optimize_team_selection_advanced(sample_drivers, sample_teams):
    """Test advanced team selection optimization."""
    drivers_df = create_driver_dataframe(sample_drivers)
    teams_df = create_team_dataframe(sample_teams)
    
    selected_drivers_df, selected_team, remaining_budget = optimize_team_selection_advanced(
        drivers_df, teams_df, budget=100.0, max_drivers=3, max_per_team=1
    )
    
    assert isinstance(selected_drivers_df, pl.DataFrame)
    assert selected_drivers_df.shape[0] <= 3  # At most 3 drivers
    
    # Check team constraint
    if not selected_drivers_df.is_empty():
        # Get the count of drivers per team
        team_counts_df = selected_drivers_df.group_by("team").agg(pl.count("id").alias("count"))
        # Verify no team has more than max_per_team drivers
        assert team_counts_df["count"].max() <= 1  # At most 1 driver per team
    
    # Check budget constraint
    total_cost = sum(selected_drivers_df["price"].to_list()) if not selected_drivers_df.is_empty() else 0.0
    if selected_team:
        total_cost += selected_team["price"]
    assert total_cost + remaining_budget == pytest.approx(100.0) 