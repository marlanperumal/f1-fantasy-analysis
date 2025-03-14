#!/usr/bin/env python3
"""
Script to create database tables for F1 Fantasy driver and constructor prices.
"""

import sqlite3
import os
import json
import pathlib
from datetime import datetime

# Get the project root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

# Ensure the data directory exists
DATA_DIR = os.path.join(ROOT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Database file path
DB_FILE = os.path.join(DATA_DIR, 'f1_fantasy.db')

def create_database():
    """Create the SQLite database and tables for F1 Fantasy prices."""
    print("Creating F1 Fantasy prices database tables...")
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    
    # Table for teams (constructors)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table for drivers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        team_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (team_id) REFERENCES teams (id)
    )
    ''')
    
    # Table for driver prices (historical)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS driver_prices (
        id INTEGER PRIMARY KEY,
        driver_id INTEGER NOT NULL,
        price REAL NOT NULL,
        effective_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (driver_id) REFERENCES drivers (id)
    )
    ''')
    
    # Table for team prices (historical)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_prices (
        id INTEGER PRIMARY KEY,
        team_id INTEGER NOT NULL,
        price REAL NOT NULL,
        effective_date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (team_id) REFERENCES teams (id)
    )
    ''')
    
    # Table for race events
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS race_events (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        circuit TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Commit the changes
    conn.commit()
    
    print("Database tables created successfully.")
    return conn

def populate_database():
    """Populate the database with driver and constructor prices."""
    print("Populating database with driver and constructor prices...")
    
    try:
        # Read the JSON files
        drivers_json_path = os.path.join(DATA_DIR, 'f1_fantasy_drivers.json')
        constructors_json_path = os.path.join(DATA_DIR, 'f1_fantasy_constructors.json')
        
        with open(drivers_json_path, "r", encoding="utf-8") as f:
            drivers_data = json.load(f)
        
        with open(constructors_json_path, "r", encoding="utf-8") as f:
            constructors_data = json.load(f)
        
        # Connect to the database
        conn = create_database()
        cursor = conn.cursor()
        
        # Insert teams (constructors)
        for constructor in constructors_data:
            # Insert team
            cursor.execute(
                'INSERT OR IGNORE INTO teams (name) VALUES (?)',
                (constructor["name"],)
            )
            
            # Get team ID
            cursor.execute('SELECT id FROM teams WHERE name = ?', (constructor["name"],))
            team_id = cursor.fetchone()[0]
            
            # Insert team price
            effective_date = datetime.fromisoformat(constructor["scrape_date"])
            cursor.execute(
                'INSERT INTO team_prices (team_id, price, effective_date) VALUES (?, ?, ?)',
                (team_id, constructor["price"], effective_date)
            )
        
        # Insert drivers
        for driver in drivers_data:
            # Get team ID
            cursor.execute('SELECT id FROM teams WHERE name = ?', (driver["team"],))
            team_id_result = cursor.fetchone()
            
            if team_id_result is None:
                # If team doesn't exist, insert it
                cursor.execute(
                    'INSERT INTO teams (name) VALUES (?)',
                    (driver["team"],)
                )
                cursor.execute('SELECT id FROM teams WHERE name = ?', (driver["team"],))
                team_id_result = cursor.fetchone()
            
            team_id = team_id_result[0]
            
            # Insert driver
            cursor.execute(
                'INSERT OR IGNORE INTO drivers (name, team_id) VALUES (?, ?)',
                (driver["name"], team_id)
            )
            
            # Get driver ID
            cursor.execute('SELECT id FROM drivers WHERE name = ?', (driver["name"],))
            driver_id = cursor.fetchone()[0]
            
            # Insert driver price
            effective_date = datetime.fromisoformat(driver["scrape_date"])
            cursor.execute(
                'INSERT INTO driver_prices (driver_id, price, effective_date) VALUES (?, ?, ?)',
                (driver_id, driver["price"], effective_date)
            )
        
        # Commit the changes
        conn.commit()
        
        print("Database populated with driver and constructor prices.")
        conn.close()
        
    except Exception as e:
        print(f"Error populating database: {e}")

if __name__ == "__main__":
    populate_database() 