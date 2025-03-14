# F1 Fantasy Data Module

This module contains the implementation of the F1 Fantasy scoring rules for the 2025 season, as well as driver and constructor prices data.

## Database Schema

The F1 Fantasy data is stored in an SQLite database (`f1_fantasy.db`) with the following tables:

### Scoring Rules Tables

- **scoring_categories**: Stores the categories of scoring rules
  - `id`: Primary key
  - `name`: Name of the category
  - `description`: Description of the category

- **scoring_rules**: Stores the individual scoring rules
  - `id`: Primary key
  - `category_id`: Foreign key to scoring_categories
  - `name`: Name of the rule
  - `points`: Points awarded for this rule
  - `description`: Description of the rule

- **qualifying_position_points**: Stores points awarded for qualifying positions
  - `position`: Qualifying position (1-20)
  - `points`: Points awarded for this position

- **race_position_points**: Stores points awarded for race positions
  - `position`: Race position (1-20)
  - `points`: Points awarded for this position

- **constructor_scoring_rules**: Stores constructor-specific scoring rules
  - `id`: Primary key
  - `name`: Name of the rule
  - `points`: Points awarded for this rule
  - `description`: Description of the rule

- **price_change_rules**: Stores rules for driver/constructor price changes
  - `id`: Primary key
  - `name`: Name of the rule
  - `change`: Price change amount
  - `description`: Description of the rule

### Driver and Constructor Prices Tables

- **teams**: Stores constructor (team) information
  - `id`: Primary key
  - `name`: Team name
  - `created_at`: Timestamp when the record was created
  - `updated_at`: Timestamp when the record was last updated

- **drivers**: Stores driver information
  - `id`: Primary key
  - `name`: Driver name
  - `team_id`: Foreign key to teams
  - `created_at`: Timestamp when the record was created
  - `updated_at`: Timestamp when the record was last updated

- **driver_prices**: Stores historical driver prices
  - `id`: Primary key
  - `driver_id`: Foreign key to drivers
  - `price`: Driver price in millions
  - `effective_date`: Date when the price became effective
  - `created_at`: Timestamp when the record was created

- **team_prices**: Stores historical team prices
  - `id`: Primary key
  - `team_id`: Foreign key to teams
  - `price`: Team price in millions
  - `effective_date`: Date when the price became effective
  - `created_at`: Timestamp when the record was created

- **race_events**: Stores race event information
  - `id`: Primary key
  - `name`: Race name
  - `circuit`: Circuit name
  - `date`: Race date
  - `created_at`: Timestamp when the record was created

## Usage

### Scoring Rules

```python
from data.scoring_rules import ScoringRules

# Initialize the scoring rules
scoring_rules = ScoringRules()

# Get all scoring categories
categories = scoring_rules.get_categories()

# Get all scoring rules
rules = scoring_rules.get_rules()

# Get qualifying position points
qualifying_points = scoring_rules.get_qualifying_position_points()

# Get race position points
race_points = scoring_rules.get_race_position_points()

# Get constructor scoring rules
constructor_rules = scoring_rules.get_constructor_rules()

# Get price change rules
price_change_rules = scoring_rules.get_price_change_rules()

# Calculate points for a driver
driver_points = scoring_rules.calculate_driver_points(
    qualifying_position=3,
    race_position=2,
    fastest_lap=True,
    driver_of_the_day=False,
    positions_gained=1,
    positions_lost=0,
    dnf=False
)
```

### Driver and Constructor Prices

```python
from data.prices import Prices
from datetime import datetime

# Initialize the prices module
prices = Prices()

# Get all drivers with their current team
drivers = prices.get_all_drivers()

# Get all teams (constructors)
teams = prices.get_all_teams()

# Get all drivers with their current prices
drivers_with_prices = prices.get_all_drivers_with_prices()

# Get all teams with their current prices
teams_with_prices = prices.get_all_teams_with_prices()

# Get a specific driver by name
driver = prices.get_driver_by_name("Max Verstappen")

# Get a specific team by name
team = prices.get_team_by_name("Ferrari")

# Get the current price of a driver
driver_price = prices.get_driver_price(driver_id=1)

# Get the price of a driver at a specific date
historical_price = prices.get_driver_price(driver_id=1, date=datetime(2025, 3, 15))

# Get the price history of a driver
price_history = prices.get_driver_price_history(driver_id=1)

# Add a new price for a driver
prices.add_driver_price(driver_id=1, price=31.0, effective_date=datetime.now())

# Add a new price for a team
prices.add_team_price(team_id=1, price=26.0, effective_date=datetime.now())
```

## Scoring Rules Summary

### Qualifying Position Points
- 1st: 10 points
- 2nd: 9 points
- 3rd: 8 points
- 4th: 7 points
- 5th: 6 points
- 6th: 5 points
- 7th: 4 points
- 8th: 3 points
- 9th: 2 points
- 10th: 1 point
- 11th-20th: 0 points

### Race Position Points
- 1st: 25 points
- 2nd: 18 points
- 3rd: 15 points
- 4th: 12 points
- 5th: 10 points
- 6th: 8 points
- 7th: 6 points
- 8th: 4 points
- 9th: 2 points
- 10th: 1 point
- 11th-20th: 0 points

### Other Driver Points
- Fastest Lap: 1 point
- Driver of the Day: 2 points
- Position Gained: 1 point per position (max 10)
- Position Lost: -1 point per position (max -10)
- Did Not Finish (DNF): -15 points

### Constructor Points
- Both cars in points (top 10): 5 points
- Both cars finish: 3 points
- Beat teammate in qualifying: 2 points
- Beat teammate in race: 3 points

### Price Changes
- Qualifying 1st: +$0.1M
- Qualifying top 10: +$0.05M
- Race win: +$0.2M
- Podium finish: +$0.1M
- Points finish (top 10): +$0.05M
- DNF: -$0.1M
- Streak of 3 podiums: +$0.3M
- Streak of 5 points finishes: +$0.2M 