#!/usr/bin/env python3
"""
Test script for the F1 Fantasy scoring rules module.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.data.scoring_rules import get_scoring_rules

def test_scoring_categories():
    """Test retrieving scoring categories."""
    scoring_rules = get_scoring_rules()
    categories = scoring_rules.get_categories()
    
    print("Scoring Categories:")
    for category in categories:
        print(f"  {category.id}: {category.name} - {category.description}")
    
    assert len(categories) > 0, "No scoring categories found"

def test_scoring_rules():
    """Test retrieving scoring rules."""
    scoring_rules = get_scoring_rules()
    rules = scoring_rules.get_scoring_rules()
    
    print("\nScoring Rules:")
    for rule in rules:
        print(f"  {rule.id}: {rule.event} - {rule.points} points - {rule.description}")
    
    assert len(rules) > 0, "No scoring rules found"

def test_qualifying_position_points():
    """Test retrieving qualifying position points."""
    scoring_rules = get_scoring_rules()
    points = scoring_rules.get_qualifying_position_points()
    
    print("\nQualifying Position Points:")
    for p in points:
        print(f"  Position {p.position}: {p.points} points")
    
    assert len(points) > 0, "No qualifying position points found"
    
    # Test getting points for a specific position
    p1_points = scoring_rules.get_qualifying_position_points(1)
    print(f"\nPoints for P1 in qualifying: {p1_points}")
    assert p1_points == 10, f"Expected 10 points for P1 in qualifying, got {p1_points}"

def test_race_position_points():
    """Test retrieving race position points."""
    scoring_rules = get_scoring_rules()
    points = scoring_rules.get_race_position_points()
    
    print("\nRace Position Points:")
    for p in points:
        print(f"  Position {p.position}: {p.points} points")
    
    assert len(points) > 0, "No race position points found"
    
    # Test getting points for a specific position
    p1_points = scoring_rules.get_race_position_points(1)
    print(f"\nPoints for P1 in race: {p1_points}")
    assert p1_points == 25, f"Expected 25 points for P1 in race, got {p1_points}"

def test_constructor_rules():
    """Test retrieving constructor rules."""
    scoring_rules = get_scoring_rules()
    rules = scoring_rules.get_constructor_rules()
    
    print("\nConstructor Rules:")
    for rule in rules:
        print(f"  {rule.id}: {rule.event} - {rule.points} points - {rule.description}")
    
    assert len(rules) > 0, "No constructor rules found"

def test_price_change_rules():
    """Test retrieving price change rules."""
    scoring_rules = get_scoring_rules()
    rules = scoring_rules.get_price_change_rules()
    
    print("\nPrice Change Rules:")
    for rule in rules:
        print(f"  {rule.id}: {rule.rule} - {rule.description}")
    
    assert len(rules) > 0, "No price change rules found"

def test_calculate_driver_points():
    """Test calculating driver points."""
    scoring_rules = get_scoring_rules()
    
    # Test case 1: Race winner with fastest lap
    total_points, breakdown = scoring_rules.calculate_driver_points(
        qualifying_position=1,
        race_position=1,
        grid_position=1,
        finished_race=True,
        fastest_lap=True,
        q3_appearance=True,
        driver_of_day=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    print("\nTest Case 1: Race winner with fastest lap")
    print(f"Total points: {total_points}")
    print("Points breakdown:")
    for category, points in breakdown.items():
        print(f"  {category}: {points}")
    
    # Test case 2: DNF from a good position
    total_points, breakdown = scoring_rules.calculate_driver_points(
        qualifying_position=3,
        race_position=20,  # DNF is usually classified in last position
        grid_position=3,
        finished_race=False,
        q3_appearance=True,
        beat_teammate_qualifying=True
    )
    
    print("\nTest Case 2: DNF from a good position")
    print(f"Total points: {total_points}")
    print("Points breakdown:")
    for category, points in breakdown.items():
        print(f"  {category}: {points}")
    
    # Test case 3: Midfield driver with good recovery
    total_points, breakdown = scoring_rules.calculate_driver_points(
        qualifying_position=15,
        race_position=10,
        grid_position=15,
        finished_race=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=True
    )
    
    print("\nTest Case 3: Midfield driver with good recovery")
    print(f"Total points: {total_points}")
    print("Points breakdown:")
    for category, points in breakdown.items():
        print(f"  {category}: {points}")

if __name__ == "__main__":
    # Run all tests
    test_scoring_categories()
    test_scoring_rules()
    test_qualifying_position_points()
    test_race_position_points()
    test_constructor_rules()
    test_price_change_rules()
    test_calculate_driver_points()
    
    print("\nAll tests passed!")
    
    # Close the database connection
    get_scoring_rules().close() 