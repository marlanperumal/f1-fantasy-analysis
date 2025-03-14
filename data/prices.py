#!/usr/bin/env python3
"""
Module for accessing F1 Fantasy driver and constructor prices data.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

class Prices:
    """Class for accessing F1 Fantasy driver and constructor prices."""
    
    def __init__(self, db_path: str = 'data/f1_fantasy.db'):
        """
        Initialize the Prices class.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        
        # Ensure the database exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)
    
    def get_all_drivers(self) -> List[Dict[str, Any]]:
        """
        Get all drivers with their current team.
        
        Returns:
            List of dictionaries containing driver information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.id, d.name, t.name as team_name
            FROM drivers d
            LEFT JOIN teams t ON d.team_id = t.id
        ''')
        
        drivers = []
        for row in cursor.fetchall():
            drivers.append({
                'id': row[0],
                'name': row[1],
                'team': row[2]
            })
        
        conn.close()
        return drivers
    
    def get_all_teams(self) -> List[Dict[str, Any]]:
        """
        Get all teams (constructors).
        
        Returns:
            List of dictionaries containing team information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name FROM teams')
        
        teams = []
        for row in cursor.fetchall():
            teams.append({
                'id': row[0],
                'name': row[1]
            })
        
        conn.close()
        return teams
    
    def get_driver_price(self, driver_id: int, date: Optional[datetime] = None) -> float:
        """
        Get the price of a driver at a specific date.
        If no date is provided, returns the most recent price.
        
        Args:
            driver_id: ID of the driver
            date: Date for which to get the price (optional)
            
        Returns:
            Price of the driver
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT price
                FROM driver_prices
                WHERE driver_id = ? AND effective_date <= ?
                ORDER BY effective_date DESC
                LIMIT 1
            ''', (driver_id, date))
        else:
            cursor.execute('''
                SELECT price
                FROM driver_prices
                WHERE driver_id = ?
                ORDER BY effective_date DESC
                LIMIT 1
            ''', (driver_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            raise ValueError(f"No price found for driver ID {driver_id}")
    
    def get_team_price(self, team_id: int, date: Optional[datetime] = None) -> float:
        """
        Get the price of a team at a specific date.
        If no date is provided, returns the most recent price.
        
        Args:
            team_id: ID of the team
            date: Date for which to get the price (optional)
            
        Returns:
            Price of the team
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT price
                FROM team_prices
                WHERE team_id = ? AND effective_date <= ?
                ORDER BY effective_date DESC
                LIMIT 1
            ''', (team_id, date))
        else:
            cursor.execute('''
                SELECT price
                FROM team_prices
                WHERE team_id = ?
                ORDER BY effective_date DESC
                LIMIT 1
            ''', (team_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            raise ValueError(f"No price found for team ID {team_id}")
    
    def get_driver_price_history(self, driver_id: int) -> List[Dict[str, Any]]:
        """
        Get the price history of a driver.
        
        Args:
            driver_id: ID of the driver
            
        Returns:
            List of dictionaries containing price history
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price, effective_date
            FROM driver_prices
            WHERE driver_id = ?
            ORDER BY effective_date
        ''', (driver_id,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'price': row[0],
                'date': row[1]
            })
        
        conn.close()
        return history
    
    def get_team_price_history(self, team_id: int) -> List[Dict[str, Any]]:
        """
        Get the price history of a team.
        
        Args:
            team_id: ID of the team
            
        Returns:
            List of dictionaries containing price history
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price, effective_date
            FROM team_prices
            WHERE team_id = ?
            ORDER BY effective_date
        ''', (team_id,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'price': row[0],
                'date': row[1]
            })
        
        conn.close()
        return history
    
    def get_driver_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get driver information by name.
        
        Args:
            name: Name of the driver
            
        Returns:
            Dictionary containing driver information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.id, d.name, t.name as team_name
            FROM drivers d
            LEFT JOIN teams t ON d.team_id = t.id
            WHERE d.name = ?
        ''', (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'team': row[2]
            }
        else:
            raise ValueError(f"Driver not found: {name}")
    
    def get_team_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get team information by name.
        
        Args:
            name: Name of the team
            
        Returns:
            Dictionary containing team information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name FROM teams WHERE name = ?', (name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1]
            }
        else:
            raise ValueError(f"Team not found: {name}")
    
    def add_driver_price(self, driver_id: int, price: float, effective_date: datetime) -> None:
        """
        Add a new price for a driver.
        
        Args:
            driver_id: ID of the driver
            price: New price
            effective_date: Date when the price becomes effective
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO driver_prices (driver_id, price, effective_date)
            VALUES (?, ?, ?)
        ''', (driver_id, price, effective_date))
        
        conn.commit()
        conn.close()
    
    def add_team_price(self, team_id: int, price: float, effective_date: datetime) -> None:
        """
        Add a new price for a team.
        
        Args:
            team_id: ID of the team
            price: New price
            effective_date: Date when the price becomes effective
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO team_prices (team_id, price, effective_date)
            VALUES (?, ?, ?)
        ''', (team_id, price, effective_date))
        
        conn.commit()
        conn.close()
    
    def get_all_drivers_with_prices(self, date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get all drivers with their current prices and teams.
        
        Args:
            date: Date for which to get the prices (optional)
            
        Returns:
            List of dictionaries containing driver information with prices
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT d.id, d.name, t.name as team_name, 
                       (SELECT dp.price 
                        FROM driver_prices dp 
                        WHERE dp.driver_id = d.id AND dp.effective_date <= ? 
                        ORDER BY dp.effective_date DESC 
                        LIMIT 1) as price
                FROM drivers d
                LEFT JOIN teams t ON d.team_id = t.id
            ''', (date,))
        else:
            cursor.execute('''
                SELECT d.id, d.name, t.name as team_name, 
                       (SELECT dp.price 
                        FROM driver_prices dp 
                        WHERE dp.driver_id = d.id 
                        ORDER BY dp.effective_date DESC 
                        LIMIT 1) as price
                FROM drivers d
                LEFT JOIN teams t ON d.team_id = t.id
            ''')
        
        drivers = []
        for row in cursor.fetchall():
            drivers.append({
                'id': row[0],
                'name': row[1],
                'team': row[2],
                'price': row[3]
            })
        
        conn.close()
        return drivers
    
    def get_all_teams_with_prices(self, date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get all teams with their current prices.
        
        Args:
            date: Date for which to get the prices (optional)
            
        Returns:
            List of dictionaries containing team information with prices
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT t.id, t.name, 
                       (SELECT tp.price 
                        FROM team_prices tp 
                        WHERE tp.team_id = t.id AND tp.effective_date <= ? 
                        ORDER BY tp.effective_date DESC 
                        LIMIT 1) as price
                FROM teams t
            ''', (date,))
        else:
            cursor.execute('''
                SELECT t.id, t.name, 
                       (SELECT tp.price 
                        FROM team_prices tp 
                        WHERE tp.team_id = t.id 
                        ORDER BY tp.effective_date DESC 
                        LIMIT 1) as price
                FROM teams t
            ''')
        
        teams = []
        for row in cursor.fetchall():
            teams.append({
                'id': row[0],
                'name': row[1],
                'price': row[2]
            })
        
        conn.close()
        return teams 