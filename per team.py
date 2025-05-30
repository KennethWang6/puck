import requests
import pandas as pd
from io import StringIO

def get_team_game_logs(team_abbr, season_year):
    url = "https://www.hockey-reference.com/teams/BOS/2023_gamelog.html"
    response = requests.get(url)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text)) 
    print(f"Number of tables found: {len(tables)}")

    # The first table is usually the game logs
    game_logs = tables[0]

    # Flatten multiindex columns by joining level names
    game_logs.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in game_logs.columns]

    print(f"Original columns:\n{game_logs.columns.tolist()}")

    # Remove duplicate header rows within the table (where 'Date' column contains the string 'Date')
    date_col_candidates = [col for col in game_logs.columns if 'Date' in col]
    if not date_col_candidates:
        raise ValueError("Could not find a 'Date' column.")
    date_col = date_col_candidates[0]

    # Drop rows that are repeated headers inside the table
    game_logs = game_logs[game_logs[date_col] != 'Date']

    # Reset index
    game_logs = game_logs.reset_index(drop=True)

    # Rename some columns for easier access
    rename_map = {
        'Unnamed: 0_level_0 Rk': 'Rk',
        'Unnamed: 1_level_0 Gtm': 'Game',
        date_col: 'Date',
        'Unnamed: 4_level_0 Opp': 'Opponent',
        'Score Rslt': 'Result',
        'Score GF': 'Goals For',
        'Score GA': 'Goals Against',
        'Unnamed: 3_level_0 Unnamed: 3_level_1': 'Home/Away',
    }
    game_logs.rename(columns=rename_map, inplace=True)

    # Filter to only actual games (Results are usually 'W', 'L', 'OT', 'SO')
    valid_results = ['W', 'L', 'OT', 'SO']
    game_logs = game_logs[game_logs['Result'].isin(valid_results)]

    # Convert goals columns to numeric (coerce errors to NaN)
    game_logs['Goals For'] = pd.to_numeric(game_logs['Goals For'], errors='coerce')
    game_logs['Goals Against'] = pd.to_numeric(game_logs['Goals Against'], errors='coerce')

    # Drop any rows with missing goal data
    game_logs = game_logs.dropna(subset=['Goals For', 'Goals Against'])

    print(f"Total games fetched: {len(game_logs)}")

    # Print first few rows for inspection
    print(game_logs.head())

    return game_logs

# Example usage:
team = "BOS"  # Boston Bruins
season = 2023

logs = get_team_game_logs(team, season)

# Basic analysis
avg_goals_for = logs['Goals For'].mean()
avg_goals_against = logs['Goals Against'].mean()
home_games = logs[logs['Home/Away'] != '@']
away_games = logs[logs['Home/Away'] == '@']

avg_goals_for_home = home_games['Goals For'].mean() if not home_games.empty else 0
avg_goals_for_away = away_games['Goals For'].mean() if not away_games.empty else 0

print(f"\nAverage Goals For per game: {avg_goals_for:.2f}")
print(f"Average Goals Against per game: {avg_goals_against:.2f}")
print(f"Home games: {len(home_games)}, Away games: {len(away_games)}")
print(f"Avg Goals For at Home: {avg_goals_for_home:.2f}")
print(f"Avg Goals For Away: {avg_goals_for_away:.2f}")
