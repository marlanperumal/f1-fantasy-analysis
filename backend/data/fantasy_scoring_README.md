# F1 Fantasy Scoring System

This module provides a comprehensive system for calculating F1 Fantasy scores based on race weekend results, evaluating fantasy team performance, and finding optimal team selections.

## Data Structures

### DriverWeekendPerformance

Stores a driver's performance data for a race weekend, including:
- Qualifying data (position, Q2/Q3 appearances, beating teammate)
- Race data (grid position, race position, fastest lap, etc.)
- Calculated fields (points, points breakdown, price, value)

### ConstructorWeekendPerformance

Stores a constructor's performance data for a race weekend, including:
- Team performance (fastest pit stop, pit stop record)
- Driver performances
- Calculated fields (points, points breakdown, price, value)

### RaceWeekendResults

Stores all results from a race weekend, including:
- Race metadata (ID, name, circuit, date)
- Driver performances
- Constructor performances

### FantasyTeam

Represents a fantasy team selection, including:
- Driver IDs (5 drivers)
- Constructor IDs (2 constructors)
- Total cost
- Total points

## Key Features

### Score Calculation

- **Driver Scoring**: Calculate points for drivers based on qualifying and race performance
- **Constructor Scoring**: Calculate points for constructors based on team and driver performance
- **Fantasy Team Scoring**: Calculate total points for a fantasy team selection

### Value Analysis

- Calculate value metrics (points per million) for drivers and constructors
- Identify high-value picks for fantasy teams

### Optimal Team Selection

- **Exhaustive Search**: Find the optimal team that maximizes points while staying under budget
- **Greedy Approach**: Find a near-optimal team using a value-based greedy algorithm (faster)

## Usage Examples

```python
# Initialize the fantasy scoring system
scoring = FantasyScoring()

# Create race weekend data
weekend = RaceWeekendResults(...)

# Add driver and constructor performances
weekend.add_driver_performance(driver_perf)
weekend.add_constructor_performance(constructor_perf)

# Calculate scores for all drivers and constructors
weekend = scoring.calculate_weekend_scores(weekend)

# Calculate score for a fantasy team
fantasy_team = FantasyTeam(driver_ids={...}, constructor_ids={...})
fantasy_team = scoring.calculate_fantasy_team_score(fantasy_team, weekend)

# Find the optimal team selection
optimal_team = scoring.find_optimal_team(weekend, budget=100.0)
```

## Scoring Rules

The scoring system is based on the official F1 Fantasy scoring rules for the 2025 season, which include:

### Qualifying
- Q3 appearance: +2 points
- Q2 appearance: +1 point
- Qualifying positions: +10 to -2 points based on position

### Race
- Race positions: +25 to -2 points based on position
- Fastest lap: +5 points
- Positions gained/lost: +/-2 points per position
- Finishing race: +1 point
- DNF: -15 points
- Disqualification: -20 points

### Other
- Driver of the Day: +10 points
- Fastest pit stop (team): +5 points
- Beating teammate in qualifying: +2 points
- Beating teammate in race: +3 points

## Implementation Details

- Uses the existing `ScoringRules` class for core scoring calculations
- Retrieves current driver and constructor prices from the database
- Provides both exhaustive and greedy algorithms for optimal team selection
- Validates fantasy team composition (5 drivers, 2 constructors)

## Example Script

See `fantasy_scoring_example.py` for a complete example of how to use the fantasy scoring system, including:
1. Creating sample race weekend data
2. Calculating scores for drivers and constructors
3. Calculating total scores for fantasy teams
4. Finding optimal team selections 