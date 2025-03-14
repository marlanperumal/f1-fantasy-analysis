"""
Module for accessing F1 Fantasy scoring rules from the database.
"""

import sqlite3
import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple

# Database file path
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'f1_fantasy.db')

@dataclass
class ScoringCategory:
    """Class representing a scoring category."""
    id: int
    name: str
    description: str

@dataclass
class ScoringRule:
    """Class representing a scoring rule."""
    id: int
    category_id: int
    event: str
    points: int
    description: str

@dataclass
class PositionPoints:
    """Class representing position-based points."""
    position: int
    points: int

@dataclass
class ConstructorRule:
    """Class representing a constructor scoring rule."""
    id: int
    event: str
    points: int
    description: str

@dataclass
class PriceChangeRule:
    """Class representing a price change rule."""
    id: int
    rule: str
    description: str

class ScoringRules:
    """Class for accessing F1 Fantasy scoring rules."""
    
    def __init__(self, db_path: str = DB_FILE):
        """Initialize the ScoringRules class.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._conn = None
        
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
    
    def get_categories(self) -> List[ScoringCategory]:
        """Get all scoring categories.
        
        Returns:
            A list of ScoringCategory objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scoring_categories')
        
        categories = []
        for row in cursor.fetchall():
            categories.append(ScoringCategory(
                id=row['id'],
                name=row['name'],
                description=row['description']
            ))
        
        return categories
    
    def get_scoring_rules(self, category_id: Optional[int] = None) -> List[ScoringRule]:
        """Get scoring rules, optionally filtered by category.
        
        Args:
            category_id: Optional category ID to filter by.
            
        Returns:
            A list of ScoringRule objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if category_id is not None:
            cursor.execute('SELECT * FROM scoring_rules WHERE category_id = ?', (category_id,))
        else:
            cursor.execute('SELECT * FROM scoring_rules')
        
        rules = []
        for row in cursor.fetchall():
            rules.append(ScoringRule(
                id=row['id'],
                category_id=row['category_id'],
                event=row['event'],
                points=row['points'],
                description=row['description']
            ))
        
        return rules
    
    def get_qualifying_position_points(self, position: Optional[int] = None) -> Union[List[PositionPoints], int]:
        """Get qualifying position points.
        
        Args:
            position: Optional position to get points for.
            
        Returns:
            If position is provided, returns the points for that position.
            Otherwise, returns a list of PositionPoints objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if position is not None:
            cursor.execute('SELECT points FROM qualifying_position_points WHERE position = ?', (position,))
            row = cursor.fetchone()
            return row['points'] if row else 0
        else:
            cursor.execute('SELECT * FROM qualifying_position_points ORDER BY position')
            points = []
            for row in cursor.fetchall():
                points.append(PositionPoints(
                    position=row['position'],
                    points=row['points']
                ))
            return points
    
    def get_race_position_points(self, position: Optional[int] = None) -> Union[List[PositionPoints], int]:
        """Get race position points.
        
        Args:
            position: Optional position to get points for.
            
        Returns:
            If position is provided, returns the points for that position.
            Otherwise, returns a list of PositionPoints objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if position is not None:
            cursor.execute('SELECT points FROM race_position_points WHERE position = ?', (position,))
            row = cursor.fetchone()
            return row['points'] if row else 0
        else:
            cursor.execute('SELECT * FROM race_position_points ORDER BY position')
            points = []
            for row in cursor.fetchall():
                points.append(PositionPoints(
                    position=row['position'],
                    points=row['points']
                ))
            return points
    
    def get_constructor_rules(self) -> List[ConstructorRule]:
        """Get constructor scoring rules.
        
        Returns:
            A list of ConstructorRule objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM constructor_scoring_rules')
        
        rules = []
        for row in cursor.fetchall():
            rules.append(ConstructorRule(
                id=row['id'],
                event=row['event'],
                points=row['points'],
                description=row['description']
            ))
        
        return rules
    
    def get_price_change_rules(self) -> List[PriceChangeRule]:
        """Get price change rules.
        
        Returns:
            A list of PriceChangeRule objects.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM price_change_rules')
        
        rules = []
        for row in cursor.fetchall():
            rules.append(PriceChangeRule(
                id=row['id'],
                rule=row['rule'],
                description=row['description']
            ))
        
        return rules
    
    def calculate_driver_points(self, 
                               qualifying_position: int, 
                               race_position: int, 
                               grid_position: int,
                               finished_race: bool = True,
                               fastest_lap: bool = False,
                               q3_appearance: bool = False,
                               q2_appearance: bool = False,
                               driver_of_day: bool = False,
                               beat_teammate_qualifying: bool = False,
                               beat_teammate_race: bool = False,
                               disqualified: bool = False) -> Tuple[int, Dict[str, int]]:
        """Calculate points for a driver based on their performance.
        
        Args:
            qualifying_position: The driver's qualifying position
            race_position: The driver's race position
            grid_position: The driver's grid position (may differ from qualifying due to penalties)
            finished_race: Whether the driver finished the race
            fastest_lap: Whether the driver set the fastest lap
            q3_appearance: Whether the driver appeared in Q3
            q2_appearance: Whether the driver appeared in Q2
            driver_of_day: Whether the driver was voted Driver of the Day
            beat_teammate_qualifying: Whether the driver beat their teammate in qualifying
            beat_teammate_race: Whether the driver beat their teammate in the race
            disqualified: Whether the driver was disqualified
            
        Returns:
            A tuple containing the total points and a breakdown of points by category
        """
        points_breakdown = {}
        
        # Qualifying position points
        qualifying_points = self.get_qualifying_position_points(qualifying_position)
        points_breakdown['qualifying_position'] = qualifying_points
        
        # Q3 and Q2 appearance points
        if q3_appearance:
            q3_points = 2
            points_breakdown['q3_appearance'] = q3_points
        else:
            q3_points = 0
            
        if q2_appearance and not q3_appearance:  # Only award Q2 points if not in Q3
            q2_points = 1
            points_breakdown['q2_appearance'] = q2_points
        else:
            q2_points = 0
        
        # Race position points
        race_points = self.get_race_position_points(race_position) if not disqualified else 0
        points_breakdown['race_position'] = race_points
        
        # Positions gained/lost
        if finished_race and not disqualified:
            positions_changed = grid_position - race_position
            if positions_changed > 0:
                position_points = positions_changed * 2
                points_breakdown['positions_gained'] = position_points
            elif positions_changed < 0:
                position_points = positions_changed * 2  # Will be negative
                points_breakdown['positions_lost'] = position_points
            else:
                position_points = 0
        else:
            position_points = 0
        
        # Finishing/DNF/DSQ points
        if disqualified:
            finish_points = -20
            points_breakdown['disqualified'] = finish_points
        elif finished_race:
            finish_points = 1
            points_breakdown['finished_race'] = finish_points
        else:
            finish_points = -15
            points_breakdown['dnf'] = finish_points
        
        # Fastest lap
        if fastest_lap:
            fastest_lap_points = 5
            points_breakdown['fastest_lap'] = fastest_lap_points
        else:
            fastest_lap_points = 0
        
        # Driver of the Day
        if driver_of_day:
            dotd_points = 10
            points_breakdown['driver_of_day'] = dotd_points
        else:
            dotd_points = 0
        
        # Beat teammate
        if beat_teammate_qualifying:
            beat_qualifying_points = 2
            points_breakdown['beat_teammate_qualifying'] = beat_qualifying_points
        else:
            beat_qualifying_points = 0
            
        if beat_teammate_race:
            beat_race_points = 3
            points_breakdown['beat_teammate_race'] = beat_race_points
        else:
            beat_race_points = 0
        
        # Calculate total points
        total_points = (
            qualifying_points + 
            q3_points + 
            q2_points + 
            race_points + 
            position_points + 
            finish_points + 
            fastest_lap_points + 
            dotd_points + 
            beat_qualifying_points + 
            beat_race_points
        )
        
        return total_points, points_breakdown

# Singleton instance
_instance = None

def get_scoring_rules() -> ScoringRules:
    """Get the singleton instance of ScoringRules.
    
    Returns:
        The ScoringRules instance.
    """
    global _instance
    if _instance is None:
        _instance = ScoringRules()
    return _instance 