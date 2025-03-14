"""
Example script demonstrating how to use the F1 Fantasy Scoring System.

This script creates sample race weekend data and shows how to:
1. Calculate scores for drivers and constructors
2. Calculate total scores for fantasy teams
3. Calculate value metrics for drivers and constructors
4. Find optimal team selections
"""

import sqlite3
import os
from datetime import datetime
from pprint import pprint

from .fantasy_scoring import (
    DriverWeekendPerformance,
    ConstructorWeekendPerformance,
    RaceWeekendResults,
    FantasyTeam,
    FantasyScoring
)

def get_driver_id_by_name(db_path, driver_name):
    """Get a driver's ID by their name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM drivers WHERE name = ?', (driver_name,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result['id']
    return None

def get_team_id_by_name(db_path, team_name):
    """Get a team's ID by their name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM teams WHERE name = ?', (team_name,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result['id']
    return None

def create_sample_race_weekend():
    """Create a sample race weekend with fictional results."""
    # Database file path
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'f1_fantasy.db')
    
    # Create a race weekend
    weekend = RaceWeekendResults(
        race_id=1,
        race_name="Bahrain Grand Prix",
        circuit="Bahrain International Circuit",
        date=datetime(2025, 3, 2)
    )
    
    # Create driver performances
    # Red Bull
    verstappen_id = get_driver_id_by_name(db_path, "Max Verstappen")
    perez_id = get_driver_id_by_name(db_path, "Sergio Perez")
    redbull_id = get_team_id_by_name(db_path, "Red Bull Racing")
    
    verstappen_perf = DriverWeekendPerformance(
        driver_id=verstappen_id,
        driver_name="Max Verstappen",
        team_id=redbull_id,
        qualifying_position=1,
        grid_position=1,
        race_position=1,
        q3_appearance=True,
        beat_teammate_qualifying=True,
        fastest_lap=True,
        driver_of_day=True,
        beat_teammate_race=True
    )
    
    perez_perf = DriverWeekendPerformance(
        driver_id=perez_id,
        driver_name="Sergio Perez",
        team_id=redbull_id,
        qualifying_position=4,
        grid_position=4,
        race_position=4,
        q3_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Ferrari
    leclerc_id = get_driver_id_by_name(db_path, "Charles Leclerc")
    sainz_id = get_driver_id_by_name(db_path, "Carlos Sainz")
    ferrari_id = get_team_id_by_name(db_path, "Ferrari")
    
    leclerc_perf = DriverWeekendPerformance(
        driver_id=leclerc_id,
        driver_name="Charles Leclerc",
        team_id=ferrari_id,
        qualifying_position=2,
        grid_position=2,
        race_position=2,
        q3_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    sainz_perf = DriverWeekendPerformance(
        driver_id=sainz_id,
        driver_name="Carlos Sainz",
        team_id=ferrari_id,
        qualifying_position=3,
        grid_position=3,
        race_position=3,
        q3_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # McLaren
    norris_id = get_driver_id_by_name(db_path, "Lando Norris")
    piastri_id = get_driver_id_by_name(db_path, "Oscar Piastri")
    mclaren_id = get_team_id_by_name(db_path, "McLaren")
    
    norris_perf = DriverWeekendPerformance(
        driver_id=norris_id,
        driver_name="Lando Norris",
        team_id=mclaren_id,
        qualifying_position=5,
        grid_position=5,
        race_position=5,
        q3_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    piastri_perf = DriverWeekendPerformance(
        driver_id=piastri_id,
        driver_name="Oscar Piastri",
        team_id=mclaren_id,
        qualifying_position=6,
        grid_position=6,
        race_position=6,
        q3_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Mercedes
    hamilton_id = get_driver_id_by_name(db_path, "Lewis Hamilton")
    russell_id = get_driver_id_by_name(db_path, "George Russell")
    mercedes_id = get_team_id_by_name(db_path, "Mercedes")
    
    hamilton_perf = DriverWeekendPerformance(
        driver_id=hamilton_id,
        driver_name="Lewis Hamilton",
        team_id=mercedes_id,
        qualifying_position=7,
        grid_position=7,
        race_position=7,
        q3_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    russell_perf = DriverWeekendPerformance(
        driver_id=russell_id,
        driver_name="George Russell",
        team_id=mercedes_id,
        qualifying_position=8,
        grid_position=8,
        race_position=8,
        q3_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Aston Martin
    alonso_id = get_driver_id_by_name(db_path, "Fernando Alonso")
    stroll_id = get_driver_id_by_name(db_path, "Lance Stroll")
    aston_id = get_team_id_by_name(db_path, "Aston Martin")
    
    alonso_perf = DriverWeekendPerformance(
        driver_id=alonso_id,
        driver_name="Fernando Alonso",
        team_id=aston_id,
        qualifying_position=9,
        grid_position=9,
        race_position=9,
        q3_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    stroll_perf = DriverWeekendPerformance(
        driver_id=stroll_id,
        driver_name="Lance Stroll",
        team_id=aston_id,
        qualifying_position=10,
        grid_position=10,
        race_position=10,
        q3_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Add more drivers with lower prices
    # RB
    tsunoda_id = get_driver_id_by_name(db_path, "Yuki Tsunoda")
    ricciardo_id = get_driver_id_by_name(db_path, "Daniel Ricciardo")
    rb_id = get_team_id_by_name(db_path, "RB")
    
    tsunoda_perf = DriverWeekendPerformance(
        driver_id=tsunoda_id,
        driver_name="Yuki Tsunoda",
        team_id=rb_id,
        qualifying_position=11,
        grid_position=11,
        race_position=11,
        q2_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    ricciardo_perf = DriverWeekendPerformance(
        driver_id=ricciardo_id,
        driver_name="Daniel Ricciardo",
        team_id=rb_id,
        qualifying_position=12,
        grid_position=12,
        race_position=12,
        q2_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Williams
    albon_id = get_driver_id_by_name(db_path, "Alexander Albon")
    williams_id = get_team_id_by_name(db_path, "Williams")
    
    albon_perf = DriverWeekendPerformance(
        driver_id=albon_id,
        driver_name="Alexander Albon",
        team_id=williams_id,
        qualifying_position=13,
        grid_position=13,
        race_position=13,
        q2_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    # Haas
    hulkenberg_id = get_driver_id_by_name(db_path, "Nico Hulkenberg")
    magnussen_id = get_driver_id_by_name(db_path, "Kevin Magnussen")
    haas_id = get_team_id_by_name(db_path, "Haas")
    
    hulkenberg_perf = DriverWeekendPerformance(
        driver_id=hulkenberg_id,
        driver_name="Nico Hulkenberg",
        team_id=haas_id,
        qualifying_position=14,
        grid_position=14,
        race_position=14,
        q2_appearance=True,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    magnussen_perf = DriverWeekendPerformance(
        driver_id=magnussen_id,
        driver_name="Kevin Magnussen",
        team_id=haas_id,
        qualifying_position=15,
        grid_position=15,
        race_position=15,
        q2_appearance=True,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Sauber
    bottas_id = get_driver_id_by_name(db_path, "Valtteri Bottas")
    zhou_id = get_driver_id_by_name(db_path, "Zhou Guanyu")
    sauber_id = get_team_id_by_name(db_path, "Sauber")
    
    bottas_perf = DriverWeekendPerformance(
        driver_id=bottas_id,
        driver_name="Valtteri Bottas",
        team_id=sauber_id,
        qualifying_position=16,
        grid_position=16,
        race_position=16,
        beat_teammate_qualifying=True,
        beat_teammate_race=True
    )
    
    zhou_perf = DriverWeekendPerformance(
        driver_id=zhou_id,
        driver_name="Zhou Guanyu",
        team_id=sauber_id,
        qualifying_position=17,
        grid_position=17,
        race_position=17,
        beat_teammate_qualifying=False,
        beat_teammate_race=False
    )
    
    # Add driver performances to the weekend
    weekend.add_driver_performance(verstappen_perf)
    weekend.add_driver_performance(perez_perf)
    weekend.add_driver_performance(leclerc_perf)
    weekend.add_driver_performance(sainz_perf)
    weekend.add_driver_performance(norris_perf)
    weekend.add_driver_performance(piastri_perf)
    weekend.add_driver_performance(hamilton_perf)
    weekend.add_driver_performance(russell_perf)
    weekend.add_driver_performance(alonso_perf)
    weekend.add_driver_performance(stroll_perf)
    weekend.add_driver_performance(tsunoda_perf)
    weekend.add_driver_performance(ricciardo_perf)
    weekend.add_driver_performance(albon_perf)
    weekend.add_driver_performance(hulkenberg_perf)
    weekend.add_driver_performance(magnussen_perf)
    weekend.add_driver_performance(bottas_perf)
    weekend.add_driver_performance(zhou_perf)
    
    # Create constructor performances
    redbull_perf = ConstructorWeekendPerformance(
        team_id=redbull_id,
        team_name="Red Bull Racing",
        fastest_pit_stop=True,
        driver_performances=[verstappen_perf, perez_perf]
    )
    
    ferrari_perf = ConstructorWeekendPerformance(
        team_id=ferrari_id,
        team_name="Ferrari",
        driver_performances=[leclerc_perf, sainz_perf]
    )
    
    mclaren_perf = ConstructorWeekendPerformance(
        team_id=mclaren_id,
        team_name="McLaren",
        driver_performances=[norris_perf, piastri_perf]
    )
    
    mercedes_perf = ConstructorWeekendPerformance(
        team_id=mercedes_id,
        team_name="Mercedes",
        driver_performances=[hamilton_perf, russell_perf]
    )
    
    aston_perf = ConstructorWeekendPerformance(
        team_id=aston_id,
        team_name="Aston Martin",
        driver_performances=[alonso_perf, stroll_perf]
    )
    
    rb_perf = ConstructorWeekendPerformance(
        team_id=rb_id,
        team_name="RB",
        driver_performances=[tsunoda_perf, ricciardo_perf]
    )
    
    williams_perf = ConstructorWeekendPerformance(
        team_id=williams_id,
        team_name="Williams",
        driver_performances=[albon_perf]
    )
    
    haas_perf = ConstructorWeekendPerformance(
        team_id=haas_id,
        team_name="Haas",
        driver_performances=[hulkenberg_perf, magnussen_perf]
    )
    
    sauber_perf = ConstructorWeekendPerformance(
        team_id=sauber_id,
        team_name="Sauber",
        driver_performances=[bottas_perf, zhou_perf]
    )
    
    # Add constructor performances to the weekend
    weekend.add_constructor_performance(redbull_perf)
    weekend.add_constructor_performance(ferrari_perf)
    weekend.add_constructor_performance(mclaren_perf)
    weekend.add_constructor_performance(mercedes_perf)
    weekend.add_constructor_performance(aston_perf)
    weekend.add_constructor_performance(rb_perf)
    weekend.add_constructor_performance(williams_perf)
    weekend.add_constructor_performance(haas_perf)
    weekend.add_constructor_performance(sauber_perf)
    
    return weekend

def main():
    """Main function to demonstrate the fantasy scoring system."""
    # Create a sample race weekend
    weekend = create_sample_race_weekend()
    
    # Initialize the fantasy scoring system
    scoring = FantasyScoring()
    
    # Calculate scores for all drivers and constructors
    weekend = scoring.calculate_weekend_scores(weekend)
    
    # Print driver scores and values
    print("\n=== DRIVER SCORES AND VALUES ===")
    for driver_id, perf in weekend.driver_performances.items():
        print(f"{perf.driver_name}: {perf.points} points, ${perf.price}M, Value: {perf.value:.2f} points/$M")
        print(f"  Breakdown: {perf.points_breakdown}")
    
    # Print constructor scores and values
    print("\n=== CONSTRUCTOR SCORES AND VALUES ===")
    for team_id, perf in weekend.constructor_performances.items():
        print(f"{perf.team_name}: {perf.points} points, ${perf.price}M, Value: {perf.value:.2f} points/$M")
        print(f"  Breakdown: {perf.points_breakdown}")
    
    # Create a sample fantasy team
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'f1_fantasy.db')
    
    # Get some driver and constructor IDs
    verstappen_id = get_driver_id_by_name(db_path, "Max Verstappen")
    leclerc_id = get_driver_id_by_name(db_path, "Charles Leclerc")
    norris_id = get_driver_id_by_name(db_path, "Lando Norris")
    hamilton_id = get_driver_id_by_name(db_path, "Lewis Hamilton")
    alonso_id = get_driver_id_by_name(db_path, "Fernando Alonso")
    
    redbull_id = get_team_id_by_name(db_path, "Red Bull Racing")
    ferrari_id = get_team_id_by_name(db_path, "Ferrari")
    
    # Create a fantasy team
    fantasy_team = FantasyTeam(
        driver_ids={verstappen_id, leclerc_id, norris_id, hamilton_id, alonso_id},
        constructor_ids={redbull_id, ferrari_id}
    )
    
    # Calculate the fantasy team's score
    fantasy_team = scoring.calculate_fantasy_team_score(fantasy_team, weekend)
    
    # Print the fantasy team's score and cost
    print("\n=== FANTASY TEAM SCORE ===")
    print(f"Total Points: {fantasy_team.total_points}")
    print(f"Total Cost: ${fantasy_team.total_cost}M")
    print(f"Note: This team exceeds the budget limit of $100M")
    
    # Find the optimal team
    print("\n=== FINDING OPTIMAL TEAM ===")
    optimal_team = scoring.find_optimal_team(weekend)
    
    if optimal_team:
        # Get driver and team names for the optimal team
        driver_names = []
        for driver_id in optimal_team.driver_ids:
            driver_perf = weekend.driver_performances[driver_id]
            driver_names.append(f"{driver_perf.driver_name} (${driver_perf.price}M, {driver_perf.points} pts)")
        
        constructor_names = []
        for team_id in optimal_team.constructor_ids:
            constructor_perf = weekend.constructor_performances[team_id]
            constructor_names.append(f"{constructor_perf.team_name} (${constructor_perf.price}M, {constructor_perf.points} pts)")
        
        print("Optimal Team:")
        print("Drivers:")
        for name in driver_names:
            print(f"  - {name}")
        
        print("Constructors:")
        for name in constructor_names:
            print(f"  - {name}")
        
        print(f"Total Points: {optimal_team.total_points}")
        print(f"Total Cost: ${optimal_team.total_cost}M")
    else:
        print("No valid team found within the budget limit.")
        print("This can happen if the total cost of even the cheapest 5 drivers and 2 constructors exceeds $100M.")
        print("Try using the greedy approach instead.")
    
    # Find a near-optimal team using the greedy approach
    print("\n=== FINDING NEAR-OPTIMAL TEAM (GREEDY) ===")
    greedy_team = scoring.find_optimal_team_greedy(weekend)
    
    if greedy_team:
        # Get driver and team names for the greedy team
        driver_names = []
        for driver_id in greedy_team.driver_ids:
            driver_perf = weekend.driver_performances[driver_id]
            driver_names.append(f"{driver_perf.driver_name} (${driver_perf.price}M, {driver_perf.points} pts)")
        
        constructor_names = []
        for team_id in greedy_team.constructor_ids:
            constructor_perf = weekend.constructor_performances[team_id]
            constructor_names.append(f"{constructor_perf.team_name} (${constructor_perf.price}M, {constructor_perf.points} pts)")
        
        print("Greedy Team:")
        print("Drivers:")
        for name in driver_names:
            print(f"  - {name}")
        
        print("Constructors:")
        for name in constructor_names:
            print(f"  - {name}")
        
        print(f"Total Points: {greedy_team.total_points}")
        print(f"Total Cost: ${greedy_team.total_cost}M")
    else:
        print("No valid team found within the budget limit using the greedy approach.")
    
    # Close the database connection
    scoring.close()

if __name__ == "__main__":
    main() 