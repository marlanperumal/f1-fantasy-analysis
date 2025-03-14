#!/usr/bin/env python3
"""
Test script for the F1 Fantasy prices module.
"""

import os
import sys
from datetime import datetime
from prices import Prices

def main():
    """Test the Prices class functionality."""
    print("Testing F1 Fantasy prices module...")
    
    # Initialize the Prices class
    try:
        prices = Prices()
        print("✓ Successfully initialized Prices class")
    except Exception as e:
        print(f"✗ Failed to initialize Prices class: {e}")
        return
    
    # Test getting all drivers
    try:
        drivers = prices.get_all_drivers()
        print(f"✓ Successfully retrieved {len(drivers)} drivers")
        print("Sample drivers:")
        for i, driver in enumerate(drivers[:3], 1):
            print(f"  {i}. {driver['name']} ({driver['team']})")
    except Exception as e:
        print(f"✗ Failed to get all drivers: {e}")
    
    # Test getting all teams
    try:
        teams = prices.get_all_teams()
        print(f"✓ Successfully retrieved {len(teams)} teams")
        print("Sample teams:")
        for i, team in enumerate(teams[:3], 1):
            print(f"  {i}. {team['name']}")
    except Exception as e:
        print(f"✗ Failed to get all teams: {e}")
    
    # Test getting all drivers with prices
    try:
        drivers_with_prices = prices.get_all_drivers_with_prices()
        print(f"✓ Successfully retrieved {len(drivers_with_prices)} drivers with prices")
        print("Sample drivers with prices:")
        for i, driver in enumerate(drivers_with_prices[:3], 1):
            print(f"  {i}. {driver['name']} ({driver['team']}) - ${driver['price']}M")
    except Exception as e:
        print(f"✗ Failed to get all drivers with prices: {e}")
    
    # Test getting all teams with prices
    try:
        teams_with_prices = prices.get_all_teams_with_prices()
        print(f"✓ Successfully retrieved {len(teams_with_prices)} teams with prices")
        print("Sample teams with prices:")
        for i, team in enumerate(teams_with_prices[:3], 1):
            print(f"  {i}. {team['name']} - ${team['price']}M")
    except Exception as e:
        print(f"✗ Failed to get all teams with prices: {e}")
    
    # Test getting a driver by name
    try:
        # Get the first driver from the list
        first_driver = drivers[0]['name']
        driver = prices.get_driver_by_name(first_driver)
        print(f"✓ Successfully retrieved driver by name: {driver['name']} ({driver['team']})")
    except Exception as e:
        print(f"✗ Failed to get driver by name: {e}")
    
    # Test getting a team by name
    try:
        # Get the first team from the list
        first_team = teams[0]['name']
        team = prices.get_team_by_name(first_team)
        print(f"✓ Successfully retrieved team by name: {team['name']}")
    except Exception as e:
        print(f"✗ Failed to get team by name: {e}")
    
    # Test getting driver price
    try:
        driver_id = drivers[0]['id']
        price = prices.get_driver_price(driver_id)
        print(f"✓ Successfully retrieved price for driver ID {driver_id}: ${price}M")
    except Exception as e:
        print(f"✗ Failed to get driver price: {e}")
    
    # Test getting team price
    try:
        team_id = teams[0]['id']
        price = prices.get_team_price(team_id)
        print(f"✓ Successfully retrieved price for team ID {team_id}: ${price}M")
    except Exception as e:
        print(f"✗ Failed to get team price: {e}")
    
    # Test getting driver price history
    try:
        driver_id = drivers[0]['id']
        history = prices.get_driver_price_history(driver_id)
        print(f"✓ Successfully retrieved price history for driver ID {driver_id}: {len(history)} entries")
    except Exception as e:
        print(f"✗ Failed to get driver price history: {e}")
    
    # Test getting team price history
    try:
        team_id = teams[0]['id']
        history = prices.get_team_price_history(team_id)
        print(f"✓ Successfully retrieved price history for team ID {team_id}: {len(history)} entries")
    except Exception as e:
        print(f"✗ Failed to get team price history: {e}")
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main() 