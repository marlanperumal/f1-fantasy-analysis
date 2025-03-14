#!/usr/bin/env python3
"""
Script to generate sample driver and constructor prices data for F1 Fantasy.
"""

import json
import os
import pathlib
from datetime import datetime

# Get the project root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

# Ensure the data directory exists
DATA_DIR = os.path.join(ROOT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Sample driver data for the 2025 F1 season
SAMPLE_DRIVERS = [
    {"name": "Max Verstappen", "team": "Red Bull Racing", "price": 30.5},
    {"name": "Lewis Hamilton", "team": "Ferrari", "price": 28.0},
    {"name": "Charles Leclerc", "team": "Ferrari", "price": 25.5},
    {"name": "Lando Norris", "team": "McLaren", "price": 24.0},
    {"name": "Oscar Piastri", "team": "McLaren", "price": 21.5},
    {"name": "George Russell", "team": "Mercedes", "price": 23.0},
    {"name": "Carlos Sainz", "team": "Williams", "price": 20.5},
    {"name": "Sergio Perez", "team": "Red Bull Racing", "price": 19.0},
    {"name": "Fernando Alonso", "team": "Aston Martin", "price": 17.5},
    {"name": "Lance Stroll", "team": "Aston Martin", "price": 12.0},
    {"name": "Pierre Gasly", "team": "Alpine", "price": 11.5},
    {"name": "Esteban Ocon", "team": "Alpine", "price": 11.0},
    {"name": "Alexander Albon", "team": "Williams", "price": 10.5},
    {"name": "Yuki Tsunoda", "team": "RB", "price": 9.0},
    {"name": "Daniel Ricciardo", "team": "RB", "price": 8.5},
    {"name": "Valtteri Bottas", "team": "Sauber", "price": 8.0},
    {"name": "Zhou Guanyu", "team": "Sauber", "price": 7.5},
    {"name": "Kevin Magnussen", "team": "Haas", "price": 7.0},
    {"name": "Nico Hulkenberg", "team": "Haas", "price": 6.5},
    {"name": "Oliver Bearman", "team": "Haas", "price": 5.5}
]

# Sample constructor data for the 2025 F1 season
SAMPLE_CONSTRUCTORS = [
    {"name": "Red Bull Racing", "price": 26.0},
    {"name": "Ferrari", "price": 25.5},
    {"name": "McLaren", "price": 24.0},
    {"name": "Mercedes", "price": 23.5},
    {"name": "Aston Martin", "price": 16.0},
    {"name": "Williams", "price": 14.5},
    {"name": "Alpine", "price": 12.0},
    {"name": "RB", "price": 10.5},
    {"name": "Haas", "price": 8.0},
    {"name": "Sauber", "price": 7.5}
]

def generate_sample_data():
    """Generate sample driver and constructor prices data."""
    print("Generating sample driver and constructor prices data...")
    
    # Add scrape date to the data
    scrape_date = datetime.now().isoformat()
    
    drivers = []
    for driver in SAMPLE_DRIVERS:
        drivers.append({
            "name": driver["name"],
            "team": driver["team"],
            "price": driver["price"],
            "scrape_date": scrape_date
        })
    
    constructors = []
    for constructor in SAMPLE_CONSTRUCTORS:
        constructors.append({
            "name": constructor["name"],
            "price": constructor["price"],
            "scrape_date": scrape_date
        })
    
    # Save the data to JSON files
    save_data_to_json(drivers, constructors)
    
    return drivers, constructors

def save_data_to_json(drivers, constructors):
    """Save the sample data to JSON files."""
    # Save driver data
    drivers_json_path = os.path.join(DATA_DIR, 'f1_fantasy_drivers.json')
    with open(drivers_json_path, "w", encoding="utf-8") as f:
        json.dump(drivers, f, indent=2)
    print(f"Sample driver data saved to {drivers_json_path}")
    
    # Save constructor data
    constructors_json_path = os.path.join(DATA_DIR, 'f1_fantasy_constructors.json')
    with open(constructors_json_path, "w", encoding="utf-8") as f:
        json.dump(constructors, f, indent=2)
    print(f"Sample constructor data saved to {constructors_json_path}")

if __name__ == "__main__":
    generate_sample_data() 