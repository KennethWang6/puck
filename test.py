import pandas as pd
import numpy as np
import glob
from datetime import timedelta
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load all team files
team_files = glob.glob("*_2025_games.csv")

# Load all data into dictionary keyed by team code (like 'CGY')
teams_data = {}
for file in team_files:
    team_code = file.split('_')[0]
    df = pd.read_csv(file, parse_dates=['Date'])
    df['Team'] = team_code
    # Convert 'Home/Away' to numeric: Home=1, Away=0
    df['Home'] = df['Home/Away'].apply(lambda x: 1 if x == 'Home' else 0)
    # Determine Win for each game: 1 if Goals For > Goals Against, else 0
    df['Win'] = (df['Goals For'] > df['Goals Against']).astype(int)
    teams_data[team_code] = df.sort_values('Date').reset_index(drop=True)

# Helper function: calculate rolling win % and avg goal diff for last N games
def rolling_stats(df, window=6):
    df['WinPctLastN'] = df['Win'].rolling(window=window, min_periods=1).mean().shift(1)
    df['GoalDiff'] = df['Goals For'] - df['Goals Against']
    df['AvgGoalDiffLastN'] = df['GoalDiff'].rolling(window=window, min_periods=1).mean().shift(1)
    return df

# Apply rolling stats to all teams
for team, df in teams_data.items():
    teams_data[team] = rolling_stats(df)

# Combine all teams into one big DataFrame
all_games = pd.concat(teams_data.values(), ignore_index=True)

# Create lookup dictionary of team-date -> rolling stats for opponents
# This helps find opponent's last 6 game stats on the date of the current game

# Build a MultiIndex for fast lookup: (Team, Date)
all_games.set_index(['Team', 'Date'], inplace=True)

def get_opponent_stats(row, stat_name):
    opp_team = row['Opponent']
    game_date = row['Date']  # <-- use the column, not index

    try:
        # Opponent's data
        opp_df = all_games[all_games['Team'] == opp_team]
        opp_stats_before = opp_df[opp_df['Date'] < game_date]
        if len(opp_stats_before) == 0:
            return np.nan
        return opp_stats_before.iloc[-1][stat_name]
    except KeyError:
        return np.nan

# Reset index to apply function row-wise
all_games = all_games.reset_index()

# Apply opponent stats columns
all_games['OppWinPctLast6'] = all_games.apply(lambda row: get_opponent_stats(row, 'WinPctLastN'), axis=1)
all_games['OppAvgGoalDiffLast6'] = all_games.apply(lambda row: get_opponent_stats(row, 'AvgGoalDiffLastN'), axis=1)

# Back-to-back game indicator (did the team play the day before?)
all_games = all_games.sort_values(['Team', 'Date'])
all_games['PrevGameDate'] = all_games.groupby('Team')['Date'].shift(1)
all_games['BackToBack'] = (all_games['Date'] - all_games['PrevGameDate'] == timedelta(days=1)).astype(int)

# Drop rows with missing opponent data (optional)
all_games = all_games.dropna(subset=['OppWinPctLast6', 'OppAvgGoalDiffLast6'])

# Features and target
features = ['WinPctLastN', 'AvgGoalDiffLastN', 'Home', 'OppWinPctLast6', 'OppAvgGoalDiffLast6', 'BackToBack']
target = 'Win'

X = all_games[features]
y = all_games[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model coefficients for interpretation
coef_df = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)
print(coef_df)