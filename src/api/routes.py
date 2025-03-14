"""API routes for F1 Fantasy Analysis."""

from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.analysis.performance import (
    analyze_form_trends,
    optimal_team_selection,
    rank_drivers_by_value,
    rank_teams_by_value,
)
from src.analysis.polars_analysis import (
    analyze_price_to_points_correlation,
    analyze_team_performance,
    create_driver_dataframe,
    create_team_dataframe,
    find_undervalued_drivers,
    optimize_team_selection_advanced,
    predict_future_points,
)
from src.data.fetcher import F1DataFetcher
from src.data.models import Driver, Race, Team
from src.utils.config import DEFAULT_BUDGET, MAX_DRIVERS

router = APIRouter(prefix="/api/v1", tags=["F1 Fantasy"])


async def get_data_fetcher() -> F1DataFetcher:
    """Dependency to get a data fetcher instance.

    Returns:
        F1DataFetcher instance
    """
    fetcher = F1DataFetcher()
    try:
        yield fetcher
    finally:
        await fetcher.close()


@router.get("/races", response_model=List[Race])
async def get_races(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get the current season's race schedule.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of Race objects
    """
    races = await fetcher.get_current_season_races()
    if not races:
        raise HTTPException(status_code=404, detail="No races found")
    return races


@router.get("/drivers", response_model=List[Driver])
async def get_drivers(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get the current drivers with fantasy data.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of Driver objects
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    return drivers


@router.get("/teams", response_model=List[Team])
async def get_teams(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get the current teams with fantasy data.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of Team objects
    """
    teams = await fetcher.get_teams()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    return teams


@router.get("/analysis/driver-value", response_model=List[Dict])
async def get_driver_value_analysis(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get driver value analysis (points per million).

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of dictionaries containing driver value analysis
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    ranked_drivers = rank_drivers_by_value(drivers)
    return [
        {
            "driver": driver.dict(),
            "value_efficiency": value_efficiency,
        }
        for driver, value_efficiency in ranked_drivers
    ]


@router.get("/analysis/team-value", response_model=List[Dict])
async def get_team_value_analysis(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get team value analysis (points per million).

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of dictionaries containing team value analysis
    """
    teams = await fetcher.get_teams()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    
    ranked_teams = rank_teams_by_value(teams)
    return [
        {
            "team": team.dict(),
            "value_efficiency": value_efficiency,
        }
        for team, value_efficiency in ranked_teams
    ]


@router.get("/analysis/form-trends", response_model=Dict[str, float])
async def get_form_trends(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get driver form trends.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        Dictionary mapping driver names to their form trend
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    return analyze_form_trends(drivers)


@router.get("/analysis/optimal-team", response_model=Dict)
async def get_optimal_team(
    budget: float = DEFAULT_BUDGET,
    max_drivers: int = MAX_DRIVERS,
    fetcher: F1DataFetcher = Depends(get_data_fetcher),
):
    """Get the optimal team selection based on value efficiency.

    Args:
        budget: Total budget available
        max_drivers: Maximum number of drivers to select
        fetcher: F1DataFetcher instance

    Returns:
        Dictionary containing the optimal team selection
    """
    drivers = await fetcher.get_drivers()
    teams = await fetcher.get_teams()
    
    if not drivers or not teams:
        raise HTTPException(status_code=404, detail="No drivers or teams found")
    
    selected_drivers, selected_team, remaining_budget = optimal_team_selection(
        drivers, teams, budget, max_drivers
    )
    
    return {
        "drivers": [driver.dict() for driver in selected_drivers],
        "team": selected_team.dict() if selected_team else None,
        "total_cost": budget - remaining_budget,
        "remaining_budget": remaining_budget,
    }


# New endpoints using Polars analysis

@router.get("/analysis/team-performance", response_model=List[Dict])
async def get_team_performance(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get team performance analysis.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        List of dictionaries containing team performance metrics
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    drivers_df = create_driver_dataframe(drivers)
    performance_df = analyze_team_performance(drivers_df)
    
    return performance_df.to_dicts()


@router.get("/analysis/price-points-correlation", response_model=Dict)
async def get_price_points_correlation(fetcher: F1DataFetcher = Depends(get_data_fetcher)):
    """Get correlation analysis between price and points.

    Args:
        fetcher: F1DataFetcher instance

    Returns:
        Dictionary with correlation metrics
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    drivers_df = create_driver_dataframe(drivers)
    return analyze_price_to_points_correlation(drivers_df)


@router.get("/analysis/undervalued-drivers", response_model=List[Dict])
async def get_undervalued_drivers(
    threshold: float = Query(0.1, description="Threshold for considering a driver undervalued"),
    fetcher: F1DataFetcher = Depends(get_data_fetcher)
):
    """Get undervalued drivers based on price-to-points ratio.

    Args:
        threshold: Threshold for considering a driver undervalued
        fetcher: F1DataFetcher instance

    Returns:
        List of dictionaries containing undervalued drivers
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    drivers_df = create_driver_dataframe(drivers)
    undervalued_df = find_undervalued_drivers(drivers_df, threshold)
    
    return undervalued_df.to_dicts()


@router.get("/analysis/predict-points", response_model=List[Dict])
async def get_predicted_points(
    races_completed: int = Query(..., description="Number of races completed"),
    races_remaining: int = Query(..., description="Number of races remaining"),
    fetcher: F1DataFetcher = Depends(get_data_fetcher)
):
    """Predict future points based on current performance.

    Args:
        races_completed: Number of races completed
        races_remaining: Number of races remaining
        fetcher: F1DataFetcher instance

    Returns:
        List of dictionaries containing predicted points
    """
    drivers = await fetcher.get_drivers()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    
    drivers_df = create_driver_dataframe(drivers)
    prediction_df = predict_future_points(drivers_df, races_completed, races_remaining)
    
    return prediction_df.to_dicts()


@router.get("/analysis/optimal-team-advanced", response_model=Dict)
async def get_optimal_team_advanced(
    budget: float = DEFAULT_BUDGET,
    max_drivers: int = MAX_DRIVERS,
    max_per_team: int = Query(2, description="Maximum number of drivers from the same team"),
    fetcher: F1DataFetcher = Depends(get_data_fetcher)
):
    """Get advanced optimal team selection with team constraints.

    Args:
        budget: Total budget available
        max_drivers: Maximum number of drivers to select
        max_per_team: Maximum number of drivers from the same team
        fetcher: F1DataFetcher instance

    Returns:
        Dictionary containing the optimal team selection
    """
    drivers = await fetcher.get_drivers()
    teams = await fetcher.get_teams()
    
    if not drivers or not teams:
        raise HTTPException(status_code=404, detail="No drivers or teams found")
    
    drivers_df = create_driver_dataframe(drivers)
    teams_df = create_team_dataframe(teams)
    
    selected_drivers_df, selected_team, remaining_budget = optimize_team_selection_advanced(
        drivers_df, teams_df, budget, max_drivers, max_per_team
    )
    
    return {
        "drivers": selected_drivers_df.to_dicts(),
        "team": selected_team,
        "total_cost": budget - remaining_budget,
        "remaining_budget": remaining_budget,
    } 