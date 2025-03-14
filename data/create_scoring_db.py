#!/usr/bin/env python3
"""
Script to create a SQLite database for F1 Fantasy scoring rules.
"""

import sqlite3
import os
import re

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Database file path
DB_FILE = 'data/f1_fantasy.db'

def create_database():
    """Create the SQLite database and tables for F1 Fantasy scoring rules."""
    print("Creating F1 Fantasy scoring database...")
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    
    # Table for scoring categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scoring_categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # Table for scoring rules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scoring_rules (
        id INTEGER PRIMARY KEY,
        category_id INTEGER NOT NULL,
        event TEXT NOT NULL,
        points INTEGER NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES scoring_categories (id)
    )
    ''')
    
    # Table for qualifying position points
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS qualifying_position_points (
        position INTEGER PRIMARY KEY,
        points INTEGER NOT NULL
    )
    ''')
    
    # Table for race position points
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS race_position_points (
        position INTEGER PRIMARY KEY,
        points INTEGER NOT NULL
    )
    ''')
    
    # Table for constructor scoring rules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS constructor_scoring_rules (
        id INTEGER PRIMARY KEY,
        event TEXT NOT NULL,
        points INTEGER NOT NULL,
        description TEXT
    )
    ''')
    
    # Table for price change rules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_change_rules (
        id INTEGER PRIMARY KEY,
        rule TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    # Commit the changes
    conn.commit()
    
    print("Database tables created successfully.")
    return conn

def populate_database(conn):
    """Populate the database with F1 Fantasy scoring rules."""
    print("Populating database with scoring rules...")
    
    cursor = conn.cursor()
    
    # Insert scoring categories
    categories = [
        (1, 'Qualifying', 'Points awarded during qualifying sessions'),
        (2, 'Race', 'Points awarded during races'),
        (3, 'Other', 'Other scoring opportunities'),
        (4, 'Constructor', 'Constructor-specific scoring rules'),
        (5, 'Price Changes', 'Rules for price changes')
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO scoring_categories (id, name, description) VALUES (?, ?, ?)',
        categories
    )
    
    # Insert qualifying position points
    qualifying_points = [
        (1, 10),   # 1st place: +10 points
        (2, 9),    # 2nd place: +9 points
        (3, 8),    # 3rd place: +8 points
        (4, 7),    # 4th place: +7 points
        (5, 6),    # 5th place: +6 points
        (6, 5),    # 6th place: +5 points
        (7, 4),    # 7th place: +4 points
        (8, 3),    # 8th place: +3 points
        (9, 2),    # 9th place: +2 points
        (10, 1),   # 10th place: +1 point
        (11, 0),   # 11th place: 0 points
        (12, 0),   # 12th place: 0 points
        (13, 0),   # 13th place: 0 points
        (14, 0),   # 14th place: 0 points
        (15, 0),   # 15th place: 0 points
        (16, -1),  # 16th place: -1 point
        (17, -1),  # 17th place: -1 point
        (18, -1),  # 18th place: -1 point
        (19, -1),  # 19th place: -1 point
        (20, -1),  # 20th place: -1 point
        (21, -2),  # 21st+ place: -2 points
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO qualifying_position_points (position, points) VALUES (?, ?)',
        qualifying_points
    )
    
    # Insert race position points
    race_points = [
        (1, 25),   # 1st place: +25 points
        (2, 18),   # 2nd place: +18 points
        (3, 15),   # 3rd place: +15 points
        (4, 12),   # 4th place: +12 points
        (5, 10),   # 5th place: +10 points
        (6, 8),    # 6th place: +8 points
        (7, 6),    # 7th place: +6 points
        (8, 4),    # 8th place: +4 points
        (9, 2),    # 9th place: +2 points
        (10, 1),   # 10th place: +1 point
        (11, 0),   # 11th place: 0 points
        (12, 0),   # 12th place: 0 points
        (13, 0),   # 13th place: 0 points
        (14, 0),   # 14th place: 0 points
        (15, 0),   # 15th place: 0 points
        (16, -1),  # 16th place: -1 point
        (17, -1),  # 17th place: -1 point
        (18, -1),  # 18th place: -1 point
        (19, -1),  # 19th place: -1 point
        (20, -1),  # 20th place: -1 point
        (21, -2),  # 21st+ place: -2 points
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO race_position_points (position, points) VALUES (?, ?)',
        race_points
    )
    
    # Insert scoring rules
    scoring_rules = [
        # Qualifying rules
        (1, 1, 'Q3 appearance', 2, 'Points for appearing in Q3'),
        (2, 1, 'Q2 appearance', 1, 'Points for appearing in Q2'),
        
        # Race rules
        (3, 2, 'Fastest lap', 5, 'Points for setting the fastest lap in the race'),
        (4, 2, 'Position gained', 2, 'Points per position gained from grid to finish'),
        (5, 2, 'Position lost', -2, 'Points per position lost from grid to finish'),
        (6, 2, 'Finishing race', 1, 'Points for finishing the race'),
        (7, 2, 'DNF', -15, 'Points for not finishing the race'),
        (8, 2, 'DSQ', -20, 'Points for disqualification'),
        
        # Other rules
        (9, 3, 'Driver of the Day', 10, 'Points for being voted Driver of the Day'),
        (10, 3, 'Fastest pit stop (team)', 5, 'Points for team with the fastest pit stop'),
        (11, 3, 'Beat teammate in qualifying', 2, 'Points for beating teammate in qualifying'),
        (12, 3, 'Beat teammate in race', 3, 'Points for beating teammate in race'),
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO scoring_rules (id, category_id, event, points, description) VALUES (?, ?, ?, ?, ?)',
        scoring_rules
    )
    
    # Insert constructor scoring rules
    constructor_rules = [
        (1, 'Driver points', 0, 'Constructor points are the sum of both drivers\' points'),
        (2, 'Fastest pit stop', 5, 'Points for the fastest pit stop'),
        (3, 'Pit stop record', 5, 'Points for setting a new pit stop record'),
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO constructor_scoring_rules (id, event, points, description) VALUES (?, ?, ?, ?)',
        constructor_rules
    )
    
    # Insert price change rules
    price_change_rules = [
        (1, 'Performance-based', 'Price changes based on performance from previous three Grands Prix'),
        (2, 'Weekly updates', 'Price changes occur after each race weekend'),
    ]
    
    cursor.executemany(
        'INSERT OR REPLACE INTO price_change_rules (id, rule, description) VALUES (?, ?, ?)',
        price_change_rules
    )
    
    # Commit the changes
    conn.commit()
    
    print("Database populated with scoring rules.")

def parse_scoring_rules_file():
    """Parse the scoring rules from the text file and populate the database."""
    try:
        # Read the scoring rules file
        with open('data/f1_fantasy_scoring_rules.txt', 'r', encoding='utf-8') as f:
            rules_text = f.read()
        
        # Create and populate the database
        conn = create_database()
        populate_database(conn)
        
        print("Database created and populated successfully.")
        conn.close()
        
    except Exception as e:
        print(f"Error parsing scoring rules: {e}")

if __name__ == "__main__":
    parse_scoring_rules_file() 