#!/usr/bin/env python3
"""
Script to scrape F1 Fantasy scoring rules from the official website
and save them to a text file.
"""

import httpx
from bs4 import BeautifulSoup
import json
import os
import re

# URL of the F1 Fantasy game rules
URL = "https://fantasy.formula1.com/en/game-rules"

# Define the scoring rules manually based on the F1 Fantasy website
# This is a fallback in case the scraping doesn't work
F1_FANTASY_SCORING_RULES = """
# F1 Fantasy Scoring Rules (2025 Season)

## Race Weekend Points

### Qualifying
- Q3 appearance: +2 points
- Q2 appearance: +1 point
- Qualifying position 1st: +10 points
- Qualifying position 2nd: +9 points
- Qualifying position 3rd: +8 points
- Qualifying position 4th: +7 points
- Qualifying position 5th: +6 points
- Qualifying position 6th: +5 points
- Qualifying position 7th: +4 points
- Qualifying position 8th: +3 points
- Qualifying position 9th: +2 points
- Qualifying position 10th: +1 point
- Qualifying position 11-15th: 0 points
- Qualifying position 16-20th: -1 point
- Qualifying position 21st+: -2 points

### Race
- Race position 1st: +25 points
- Race position 2nd: +18 points
- Race position 3rd: +15 points
- Race position 4th: +12 points
- Race position 5th: +10 points
- Race position 6th: +8 points
- Race position 7th: +6 points
- Race position 8th: +4 points
- Race position 9th: +2 points
- Race position 10th: +1 point
- Race position 11-15th: 0 points
- Race position 16-20th: -1 point
- Race position 21st+: -2 points
- Fastest lap: +5 points
- Positions gained (per position): +2 points
- Positions lost (per position): -2 points
- Finishing race: +1 point
- Not finishing race (DNF): -15 points
- Disqualification (DSQ): -20 points

### Other
- Driver of the Day: +10 points
- Fastest pit stop (team): +5 points
- Beating teammate in qualifying: +2 points
- Beating teammate in race: +3 points

## Constructors
- Constructor points are the sum of both drivers' points
- Fastest pit stop: +5 points
- Pit stop record: +5 points
- Pit stop time-based points (scaled)

## Price Changes
- Driver/Constructor prices change based on performance from previous three Grands Prix
- Price changes occur after each race weekend
"""

def scrape_scoring_rules():
    """Scrape the scoring rules from the F1 Fantasy website."""
    print("Fetching scoring rules from F1 Fantasy website...")
    
    try:
        # Make the HTTP request
        response = httpx.get(URL, follow_redirects=True)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find scoring rules sections
        # This is a best effort attempt as the structure may change
        scoring_sections = soup.find_all(['div', 'section', 'article'], 
                                        class_=re.compile('scoring|points|rules|content'))
        
        # If we can't find the scoring sections, use our predefined rules
        if not scoring_sections:
            print("Could not find scoring rules section. Using predefined rules.")
            scoring_rules = F1_FANTASY_SCORING_RULES
        else:
            # Extract the text from the scoring sections
            scoring_rules = []
            for section in scoring_sections:
                section_text = section.get_text(strip=True, separator="\n")
                if section_text:
                    scoring_rules.append(section_text)
            
            scoring_rules = "\n\n".join(scoring_rules)
        
        # Save the raw HTML for inspection
        with open("data/f1_fantasy_rules_full.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Save the scoring rules to a text file
        with open("data/f1_fantasy_scoring_rules.txt", "w", encoding="utf-8") as f:
            f.write(scoring_rules)
        
        print(f"Scoring rules saved to data/f1_fantasy_scoring_rules.txt")
        return scoring_rules
    
    except Exception as e:
        print(f"Error scraping scoring rules: {e}")
        
        # Use predefined rules as fallback
        print("Using predefined scoring rules as fallback.")
        with open("data/f1_fantasy_scoring_rules.txt", "w", encoding="utf-8") as f:
            f.write(F1_FANTASY_SCORING_RULES)
        
        print(f"Fallback scoring rules saved to data/f1_fantasy_scoring_rules.txt")
        return F1_FANTASY_SCORING_RULES

if __name__ == "__main__":
    scrape_scoring_rules() 