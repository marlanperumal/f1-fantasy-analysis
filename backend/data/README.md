# F1 Fantasy Scoring Rules

This module provides access to the F1 Fantasy scoring rules for the 2025 season. The rules are stored in a SQLite database and can be accessed through the `ScoringRules` class.

## Database Schema

The scoring rules are stored in the following tables:

- `scoring_categories`: Categories of scoring rules (Qualifying, Race, Other, Constructor, Price Changes)
- `scoring_rules`: Individual scoring rules with points values
- `qualifying_position_points`: Points awarded for qualifying positions
- `race_position_points`: Points awarded for race positions
- `constructor_scoring_rules`: Constructor-specific scoring rules
- `price_change_rules`: Rules for price changes

## Usage

```python
from backend.data.scoring_rules import get_scoring_rules

# Get the singleton instance of ScoringRules
scoring_rules = get_scoring_rules()

# Get all scoring categories
categories = scoring_rules.get_categories()

# Get all scoring rules
rules = scoring_rules.get_scoring_rules()

# Get scoring rules for a specific category (e.g., Qualifying)
qualifying_rules = scoring_rules.get_scoring_rules(category_id=1)

# Get points for qualifying positions
qualifying_points = scoring_rules.get_qualifying_position_points()

# Get points for a specific qualifying position
p1_qualifying_points = scoring_rules.get_qualifying_position_points(1)  # 10 points

# Get points for race positions
race_points = scoring_rules.get_race_position_points()

# Get points for a specific race position
p1_race_points = scoring_rules.get_race_position_points(1)  # 25 points

# Get constructor scoring rules
constructor_rules = scoring_rules.get_constructor_rules()

# Get price change rules
price_change_rules = scoring_rules.get_price_change_rules()

# Calculate points for a driver
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

# Close the database connection when done
scoring_rules.close()
```

## Scoring Rules Summary

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

### Constructors
- Constructor points are the sum of both drivers' points
- Fastest pit stop: +5 points
- Pit stop record: +5 points
- Pit stop time-based points (scaled)

### Price Changes
- Driver/Constructor prices change based on performance from previous three Grands Prix
- Price changes occur after each race weekend 