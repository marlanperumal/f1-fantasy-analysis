"""
F1 Fantasy Scoring System

This module provides data structures and methods for:
1. Storing race weekend data needed for scoring
2. Calculating scores for drivers and constructors
3. Calculating total scores for fantasy teams
4. Calculating value metrics for drivers and constructors
5. Finding optimal team selections
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import sqlite3
import os
from itertools import combinations
import heapq

from .scoring_rules import ScoringRules, get_scoring_rules

# Database file path
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'f1_fantasy.db')

@dataclass
class DriverWeekendPerformance:
    """Data structure to store a driver's performance for a race weekend."""
    driver_id: int
    driver_name: str
    team_id: int
    
    # Required race data
    qualifying_position: int
    grid_position: int  # May differ from qualifying due to penalties
    race_position: int
    
    # Optional qualifying data
    q3_appearance: bool = False
    q2_appearance: bool = False
    beat_teammate_qualifying: bool = False
    
    # Optional race data
    finished_race: bool = True
    fastest_lap: bool = False
    driver_of_day: bool = False
    beat_teammate_race: bool = False
    disqualified: bool = False
    
    # Calculated fields
    points: int = 0
    points_breakdown: Dict[str, int] = field(default_factory=dict)
    price: float = 0.0
    value: float = 0.0  # Points per million


@dataclass
class ConstructorWeekendPerformance:
    """Data structure to store a constructor's performance for a race weekend."""
    team_id: int
    team_name: str
    
    # Team performance
    fastest_pit_stop: bool = False
    pit_stop_record: bool = False
    
    # Driver performances
    driver_performances: List[DriverWeekendPerformance] = field(default_factory=list)
    
    # Calculated fields
    points: int = 0
    points_breakdown: Dict[str, int] = field(default_factory=dict)
    price: float = 0.0
    value: float = 0.0  # Points per million


@dataclass
class RaceWeekendResults:
    """Data structure to store all results from a race weekend."""
    race_id: int
    race_name: str
    circuit: str
    date: datetime
    
    driver_performances: Dict[int, DriverWeekendPerformance] = field(default_factory=dict)
    constructor_performances: Dict[int, ConstructorWeekendPerformance] = field(default_factory=dict)
    
    def add_driver_performance(self, performance: DriverWeekendPerformance) -> None:
        """Add a driver performance to the race weekend results."""
        self.driver_performances[performance.driver_id] = performance
    
    def add_constructor_performance(self, performance: ConstructorWeekendPerformance) -> None:
        """Add a constructor performance to the race weekend results."""
        self.constructor_performances[performance.team_id] = performance


@dataclass
class FantasyTeam:
    """Data structure to represent a fantasy team selection."""
    driver_ids: Set[int]
    constructor_ids: Set[int]
    total_cost: float = 0.0
    total_points: int = 0
    
    def __post_init__(self):
        """Validate the fantasy team composition."""
        if len(self.driver_ids) != 5:
            raise ValueError("Fantasy team must have exactly 5 drivers")
        if len(self.constructor_ids) != 2:
            raise ValueError("Fantasy team must have exactly 2 constructors")


class FantasyScoring:
    """Class for calculating F1 Fantasy scores and optimal team selections."""
    
    def __init__(self, db_path: str = DB_FILE):
        """Initialize the FantasyScoring class.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._conn = None
        self.scoring_rules = get_scoring_rules()
        
    def _get_connection(self) -> sqlite3.Connection:
        """Get a connection to the database.
        
        Returns:
            A SQLite connection object.
        """
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    def close(self):
        """Close the database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            
    def get_driver_price(self, driver_id: int) -> float:
        """Get the current price of a driver.
        
        Args:
            driver_id: The ID of the driver.
            
        Returns:
            The current price of the driver in millions.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get the most recent price for the driver
        cursor.execute('''
            SELECT price 
            FROM driver_prices 
            WHERE driver_id = ? 
            ORDER BY effective_date DESC 
            LIMIT 1
        ''', (driver_id,))
        
        result = cursor.fetchone()
        if result:
            return result['price']
        return 0.0
    
    def get_constructor_price(self, team_id: int) -> float:
        """Get the current price of a constructor.
        
        Args:
            team_id: The ID of the constructor.
            
        Returns:
            The current price of the constructor in millions.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get the most recent price for the constructor
        cursor.execute('''
            SELECT price 
            FROM team_prices 
            WHERE team_id = ? 
            ORDER BY effective_date DESC 
            LIMIT 1
        ''', (team_id,))
        
        result = cursor.fetchone()
        if result:
            return result['price']
        return 0.0
    
    def calculate_driver_score(self, performance: DriverWeekendPerformance) -> DriverWeekendPerformance:
        """Calculate the score for a driver based on their weekend performance.
        
        Args:
            performance: The driver's weekend performance data.
            
        Returns:
            The updated driver performance with calculated points.
        """
        # Calculate points using the scoring rules
        total_points, points_breakdown = self.scoring_rules.calculate_driver_points(
            qualifying_position=performance.qualifying_position,
            race_position=performance.race_position,
            grid_position=performance.grid_position,
            finished_race=performance.finished_race,
            fastest_lap=performance.fastest_lap,
            q3_appearance=performance.q3_appearance,
            q2_appearance=performance.q2_appearance,
            driver_of_day=performance.driver_of_day,
            beat_teammate_qualifying=performance.beat_teammate_qualifying,
            beat_teammate_race=performance.beat_teammate_race,
            disqualified=performance.disqualified
        )
        
        # Update the performance object
        performance.points = total_points
        performance.points_breakdown = points_breakdown
        
        # Get the driver's price
        performance.price = self.get_driver_price(performance.driver_id)
        
        # Calculate value (points per million)
        if performance.price > 0:
            performance.value = performance.points / performance.price
        else:
            performance.value = 0.0
            
        return performance
    
    def calculate_constructor_score(self, performance: ConstructorWeekendPerformance) -> ConstructorWeekendPerformance:
        """Calculate the score for a constructor based on their weekend performance.
        
        Args:
            performance: The constructor's weekend performance data.
            
        Returns:
            The updated constructor performance with calculated points.
        """
        points_breakdown = {}
        total_points = 0
        
        # Sum up the points from both drivers
        for driver_perf in performance.driver_performances:
            total_points += driver_perf.points
        
        points_breakdown['driver_points'] = total_points
        
        # Add points for constructor-specific achievements
        if performance.fastest_pit_stop:
            pit_stop_points = 5
            points_breakdown['fastest_pit_stop'] = pit_stop_points
            total_points += pit_stop_points
            
        if performance.pit_stop_record:
            record_points = 5
            points_breakdown['pit_stop_record'] = record_points
            total_points += record_points
        
        # Update the performance object
        performance.points = total_points
        performance.points_breakdown = points_breakdown
        
        # Get the constructor's price
        performance.price = self.get_constructor_price(performance.team_id)
        
        # Calculate value (points per million)
        if performance.price > 0:
            performance.value = performance.points / performance.price
        else:
            performance.value = 0.0
            
        return performance
    
    def calculate_weekend_scores(self, weekend: RaceWeekendResults) -> RaceWeekendResults:
        """Calculate scores for all drivers and constructors for a race weekend.
        
        Args:
            weekend: The race weekend results.
            
        Returns:
            The updated race weekend results with calculated scores.
        """
        # Calculate scores for all drivers
        for driver_id, performance in weekend.driver_performances.items():
            self.calculate_driver_score(performance)
        
        # Calculate scores for all constructors
        for team_id, performance in weekend.constructor_performances.items():
            self.calculate_constructor_score(performance)
            
        return weekend
    
    def calculate_fantasy_team_score(self, team: FantasyTeam, weekend: RaceWeekendResults) -> FantasyTeam:
        """Calculate the total score for a fantasy team for a race weekend.
        
        Args:
            team: The fantasy team.
            weekend: The race weekend results.
            
        Returns:
            The updated fantasy team with calculated total score and cost.
        """
        total_points = 0
        total_cost = 0.0
        
        # Add up driver points and costs
        for driver_id in team.driver_ids:
            if driver_id in weekend.driver_performances:
                driver_perf = weekend.driver_performances[driver_id]
                total_points += driver_perf.points
                total_cost += driver_perf.price
        
        # Add up constructor points and costs
        for team_id in team.constructor_ids:
            if team_id in weekend.constructor_performances:
                constructor_perf = weekend.constructor_performances[team_id]
                total_points += constructor_perf.points
                total_cost += constructor_perf.price
        
        # Update the fantasy team
        team.total_points = total_points
        team.total_cost = total_cost
        
        return team
    
    def find_optimal_team(self, weekend: RaceWeekendResults, budget: float = 100.0) -> Optional[FantasyTeam]:
        """Find the optimal fantasy team selection that maximizes points while staying under budget.
        
        Args:
            weekend: The race weekend results.
            budget: The maximum budget for the team in millions.
            
        Returns:
            The optimal fantasy team selection, or None if no valid team can be formed within budget.
        """
        # Get all drivers and constructors with their points and prices
        drivers = [(d.driver_id, d.points, d.price) for d in weekend.driver_performances.values()]
        constructors = [(c.team_id, c.points, c.price) for c in weekend.constructor_performances.values()]
        
        # Sort by points (descending) for better pruning
        drivers.sort(key=lambda x: x[1], reverse=True)
        constructors.sort(key=lambda x: x[1], reverse=True)
        
        best_team = None
        best_points = -1
        
        # Try all combinations of 5 drivers
        for driver_combo in combinations(drivers, 5):
            driver_ids = {d[0] for d in driver_combo}
            driver_points = sum(d[1] for d in driver_combo)
            driver_cost = sum(d[2] for d in driver_combo)
            
            # If drivers already exceed budget, skip
            if driver_cost > budget:
                continue
            
            # Try all combinations of 2 constructors
            for constructor_combo in combinations(constructors, 2):
                constructor_ids = {c[0] for c in constructor_combo}
                constructor_points = sum(c[1] for c in constructor_combo)
                constructor_cost = sum(c[2] for c in constructor_combo)
                
                total_cost = driver_cost + constructor_cost
                total_points = driver_points + constructor_points
                
                # Check if this team is valid and better than our current best
                if total_cost <= budget and total_points > best_points:
                    best_points = total_points
                    best_team = FantasyTeam(
                        driver_ids=driver_ids,
                        constructor_ids=constructor_ids,
                        total_cost=total_cost,
                        total_points=total_points
                    )
        
        return best_team
    
    def find_optimal_team_greedy(self, weekend: RaceWeekendResults, budget: float = 100.0) -> Optional[FantasyTeam]:
        """Find a near-optimal fantasy team using a greedy approach based on value (points per million).
        
        This is a faster alternative to the exhaustive search in find_optimal_team.
        
        Args:
            weekend: The race weekend results.
            budget: The maximum budget for the team in millions.
            
        Returns:
            A high-scoring fantasy team selection, or None if no valid team can be formed within budget.
        """
        # Get all drivers and constructors with their points, prices, and values
        drivers = [(d.driver_id, d.points, d.price, d.value) for d in weekend.driver_performances.values()]
        constructors = [(c.team_id, c.points, c.price, c.value) for c in weekend.constructor_performances.values()]
        
        # Sort by value (points per million) in descending order
        drivers.sort(key=lambda x: x[3], reverse=True)
        constructors.sort(key=lambda x: x[3], reverse=True)
        
        # Select top 5 drivers by value that fit within budget
        selected_drivers = []
        remaining_budget = budget
        
        for driver in drivers:
            if len(selected_drivers) < 5 and driver[2] <= remaining_budget:
                selected_drivers.append(driver)
                remaining_budget -= driver[2]
        
        # If we couldn't select 5 drivers, try a different approach
        if len(selected_drivers) < 5:
            # Sort by points in descending order
            drivers.sort(key=lambda x: x[1], reverse=True)
            
            # Start with an empty selection
            selected_drivers = []
            remaining_budget = budget
            
            # Greedily select drivers by points
            for driver in drivers:
                if len(selected_drivers) < 5 and driver[2] <= remaining_budget:
                    selected_drivers.append(driver)
                    remaining_budget -= driver[2]
            
            # If we still couldn't select 5 drivers, try selecting the cheapest drivers
            if len(selected_drivers) < 5:
                # Sort by price in ascending order
                drivers.sort(key=lambda x: x[2])
                
                # Start with an empty selection
                selected_drivers = []
                remaining_budget = budget
                
                # Select the cheapest drivers
                for driver in drivers:
                    if len(selected_drivers) < 5 and driver[2] <= remaining_budget:
                        selected_drivers.append(driver)
                        remaining_budget -= driver[2]
        
        # If we still couldn't select 5 drivers, return None
        if len(selected_drivers) < 5:
            return None
        
        # Select top 2 constructors by value that fit within remaining budget
        selected_constructors = []
        
        for constructor in constructors:
            if len(selected_constructors) < 2 and constructor[2] <= remaining_budget:
                selected_constructors.append(constructor)
                remaining_budget -= constructor[2]
        
        # If we couldn't select 2 constructors, try a different approach
        if len(selected_constructors) < 2:
            # Sort by points in descending order
            constructors.sort(key=lambda x: x[1], reverse=True)
            
            # Start with an empty selection
            selected_constructors = []
            
            # Calculate remaining budget after selected drivers
            remaining_budget = budget - sum(driver[2] for driver in selected_drivers)
            
            # Greedily select constructors by points
            for constructor in constructors:
                if len(selected_constructors) < 2 and constructor[2] <= remaining_budget:
                    selected_constructors.append(constructor)
                    remaining_budget -= constructor[2]
            
            # If we still couldn't select 2 constructors, try selecting the cheapest constructors
            if len(selected_constructors) < 2:
                # Sort by price in ascending order
                constructors.sort(key=lambda x: x[2])
                
                # Start with an empty selection
                selected_constructors = []
                
                # Calculate remaining budget after selected drivers
                remaining_budget = budget - sum(driver[2] for driver in selected_drivers)
                
                # Select the cheapest constructors
                for constructor in constructors:
                    if len(selected_constructors) < 2 and constructor[2] <= remaining_budget:
                        selected_constructors.append(constructor)
                        remaining_budget -= constructor[2]
        
        # If we still couldn't select 2 constructors, return None
        if len(selected_constructors) < 2:
            return None
        
        # Create and return the fantasy team
        return FantasyTeam(
            driver_ids={driver[0] for driver in selected_drivers},
            constructor_ids={constructor[0] for constructor in selected_constructors},
            total_cost=budget - remaining_budget,
            total_points=sum(driver[1] for driver in selected_drivers) + sum(constructor[1] for constructor in selected_constructors)
        ) 