#!/usr/bin/env python3
"""
Script to scrape current driver and constructor prices from the F1 Fantasy website.
"""

import httpx
from bs4 import BeautifulSoup
import json
import os
import re
import pathlib
from datetime import datetime
import time

# Get the project root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent

# Ensure the data directory exists
DATA_DIR = os.path.join(ROOT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# URLs for the F1 Fantasy statistics pages
DRIVER_URL = "https://fantasy.formula1.com/en/statistics/details?tab=driver"
CONSTRUCTOR_URL = "https://fantasy.formula1.com/en/statistics/details?tab=constructor"

def scrape_prices():
    """Scrape current driver and constructor prices from the F1 Fantasy website."""
    print("Fetching current driver and constructor prices...")
    
    drivers = []
    constructors = []
    
    try:
        # Scrape driver prices
        print("Scraping driver prices...")
        driver_data = scrape_driver_prices()
        if driver_data:
            drivers = driver_data
            print(f"Successfully scraped data for {len(drivers)} drivers")
        else:
            print("Failed to scrape driver prices")
        
        # Scrape constructor prices
        print("Scraping constructor prices...")
        constructor_data = scrape_constructor_prices()
        if constructor_data:
            constructors = constructor_data
            print(f"Successfully scraped data for {len(constructors)} constructors")
        else:
            print("Failed to scrape constructor prices")
        
        # Save the data to JSON files
        save_data_to_json(drivers, constructors)
        
        return drivers, constructors
    
    except Exception as e:
        print(f"Error scraping prices: {e}")
        return None, None

def scrape_driver_prices():
    """Scrape driver prices from the F1 Fantasy website."""
    try:
        # Make the HTTP request
        response = httpx.get(DRIVER_URL, follow_redirects=True)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the data in the page
        # First, look for JavaScript data embedded in the page
        scripts = soup.find_all('script')
        driver_data = []
        
        for script in scripts:
            script_text = script.string
            if script_text and 'window.__INITIAL_STATE__' in script_text:
                # Extract the JSON data
                match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script_text, re.DOTALL)
                if match:
                    json_data = match.group(1)
                    try:
                        data = json.loads(json_data)
                        # Extract driver data from the JSON
                        if 'statistics' in data and 'drivers' in data['statistics']:
                            driver_data = data['statistics']['drivers']
                            break
                    except json.JSONDecodeError:
                        continue
        
        # If we couldn't find the data in the scripts, try to parse the table directly
        if not driver_data:
            driver_table = soup.find('table', class_=re.compile('drivers|statistics'))
            if driver_table:
                rows = driver_table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        name = cols[0].text.strip()
                        team = cols[1].text.strip()
                        price = cols[2].text.strip().replace('$', '').replace('m', '')
                        driver_data.append({
                            'name': name,
                            'team': team,
                            'price': float(price),
                            'scrape_date': datetime.now().isoformat()
                        })
        
        # Save the raw HTML for inspection
        drivers_html_path = os.path.join(DATA_DIR, 'f1_fantasy_drivers_page.html')
        with open(drivers_html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Process the driver data
        processed_drivers = []
        for driver in driver_data:
            # Extract the relevant fields
            processed_driver = {
                'name': driver.get('name', ''),
                'team': driver.get('team', ''),
                'price': driver.get('price', 0),
                'scrape_date': datetime.now().isoformat()
            }
            processed_drivers.append(processed_driver)
        
        return processed_drivers
    
    except Exception as e:
        print(f"Error scraping driver prices: {e}")
        return []

def scrape_constructor_prices():
    """Scrape constructor prices from the F1 Fantasy website."""
    try:
        # Make the HTTP request
        response = httpx.get(CONSTRUCTOR_URL, follow_redirects=True)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the data in the page
        # First, look for JavaScript data embedded in the page
        scripts = soup.find_all('script')
        constructor_data = []
        
        for script in scripts:
            script_text = script.string
            if script_text and 'window.__INITIAL_STATE__' in script_text:
                # Extract the JSON data
                match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script_text, re.DOTALL)
                if match:
                    json_data = match.group(1)
                    try:
                        data = json.loads(json_data)
                        # Extract constructor data from the JSON
                        if 'statistics' in data and 'constructors' in data['statistics']:
                            constructor_data = data['statistics']['constructors']
                            break
                    except json.JSONDecodeError:
                        continue
        
        # If we couldn't find the data in the scripts, try to parse the table directly
        if not constructor_data:
            constructor_table = soup.find('table', class_=re.compile('constructors|statistics'))
            if constructor_table:
                rows = constructor_table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        name = cols[0].text.strip()
                        price = cols[1].text.strip().replace('$', '').replace('m', '')
                        constructor_data.append({
                            'name': name,
                            'price': float(price),
                            'scrape_date': datetime.now().isoformat()
                        })
        
        # Save the raw HTML for inspection
        constructors_html_path = os.path.join(DATA_DIR, 'f1_fantasy_constructors_page.html')
        with open(constructors_html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Process the constructor data
        processed_constructors = []
        for constructor in constructor_data:
            # Extract the relevant fields
            processed_constructor = {
                'name': constructor.get('name', ''),
                'price': constructor.get('price', 0),
                'scrape_date': datetime.now().isoformat()
            }
            processed_constructors.append(processed_constructor)
        
        return processed_constructors
    
    except Exception as e:
        print(f"Error scraping constructor prices: {e}")
        return []

def save_data_to_json(drivers, constructors):
    """Save the scraped data to JSON files."""
    # Save driver data
    if drivers:
        drivers_json_path = os.path.join(DATA_DIR, 'f1_fantasy_drivers.json')
        with open(drivers_json_path, "w", encoding="utf-8") as f:
            json.dump(drivers, f, indent=2)
        print(f"Driver data saved to {drivers_json_path}")
    
    # Save constructor data
    if constructors:
        constructors_json_path = os.path.join(DATA_DIR, 'f1_fantasy_constructors.json')
        with open(constructors_json_path, "w", encoding="utf-8") as f:
            json.dump(constructors, f, indent=2)
        print(f"Constructor data saved to {constructors_json_path}")

if __name__ == "__main__":
    scrape_prices() 