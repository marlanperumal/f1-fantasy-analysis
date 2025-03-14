#!/usr/bin/env python3
"""
Test script for the F1 Fantasy prices module.
"""

import os
import sys
import unittest
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.data.prices import Prices

class TestPrices(unittest.TestCase):
    """Test cases for the Prices class."""
    
    def setUp(self):
        """Set up the test environment."""
        self.prices = Prices()
    
    def test_initialization(self):
        """Test that the Prices class can be initialized."""
        self.assertIsInstance(self.prices, Prices)
    
    def test_get_all_drivers(self):
        """Test getting all drivers."""
        drivers = self.prices.get_all_drivers()
        self.assertIsInstance(drivers, list)
        self.assertGreater(len(drivers), 0)
        
        # Check the structure of the driver data
        driver = drivers[0]
        self.assertIn('id', driver)
        self.assertIn('name', driver)
        self.assertIn('team', driver)
    
    def test_get_all_teams(self):
        """Test getting all teams."""
        teams = self.prices.get_all_teams()
        self.assertIsInstance(teams, list)
        self.assertGreater(len(teams), 0)
        
        # Check the structure of the team data
        team = teams[0]
        self.assertIn('id', team)
        self.assertIn('name', team)
    
    def test_get_all_drivers_with_prices(self):
        """Test getting all drivers with prices."""
        drivers = self.prices.get_all_drivers_with_prices()
        self.assertIsInstance(drivers, list)
        self.assertGreater(len(drivers), 0)
        
        # Check the structure of the driver data
        driver = drivers[0]
        self.assertIn('id', driver)
        self.assertIn('name', driver)
        self.assertIn('team', driver)
        self.assertIn('price', driver)
    
    def test_get_all_teams_with_prices(self):
        """Test getting all teams with prices."""
        teams = self.prices.get_all_teams_with_prices()
        self.assertIsInstance(teams, list)
        self.assertGreater(len(teams), 0)
        
        # Check the structure of the team data
        team = teams[0]
        self.assertIn('id', team)
        self.assertIn('name', team)
        self.assertIn('price', team)
    
    def test_get_driver_by_name(self):
        """Test getting a driver by name."""
        # Get the first driver from the list
        drivers = self.prices.get_all_drivers()
        first_driver_name = drivers[0]['name']
        
        # Get the driver by name
        driver = self.prices.get_driver_by_name(first_driver_name)
        self.assertEqual(driver['name'], first_driver_name)
    
    def test_get_team_by_name(self):
        """Test getting a team by name."""
        # Get the first team from the list
        teams = self.prices.get_all_teams()
        first_team_name = teams[0]['name']
        
        # Get the team by name
        team = self.prices.get_team_by_name(first_team_name)
        self.assertEqual(team['name'], first_team_name)
    
    def test_get_driver_price(self):
        """Test getting a driver's price."""
        # Get the first driver from the list
        drivers = self.prices.get_all_drivers()
        driver_id = drivers[0]['id']
        
        # Get the driver's price
        price = self.prices.get_driver_price(driver_id)
        self.assertIsInstance(price, (int, float))
    
    def test_get_team_price(self):
        """Test getting a team's price."""
        # Get the first team from the list
        teams = self.prices.get_all_teams()
        team_id = teams[0]['id']
        
        # Get the team's price
        price = self.prices.get_team_price(team_id)
        self.assertIsInstance(price, (int, float))
    
    def test_get_driver_price_history(self):
        """Test getting a driver's price history."""
        # Get the first driver from the list
        drivers = self.prices.get_all_drivers()
        driver_id = drivers[0]['id']
        
        # Get the driver's price history
        history = self.prices.get_driver_price_history(driver_id)
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Check the structure of the history data
        entry = history[0]
        self.assertIn('price', entry)
        self.assertIn('date', entry)
    
    def test_get_team_price_history(self):
        """Test getting a team's price history."""
        # Get the first team from the list
        teams = self.prices.get_all_teams()
        team_id = teams[0]['id']
        
        # Get the team's price history
        history = self.prices.get_team_price_history(team_id)
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Check the structure of the history data
        entry = history[0]
        self.assertIn('price', entry)
        self.assertIn('date', entry)

def run_tests():
    """Run the tests."""
    unittest.main()

if __name__ == "__main__":
    run_tests() 