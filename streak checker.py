import pandas as pd


t = ["ANA", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "UTA", "VAN", "VEG", "WPG", "WSH"] 
# Load your CSV file

for team in t:

    df = pd.read_csv(team + '_2025_games.csv')

    # The "Streak" column usually looks like "W2", "L3", "W1", etc.
    # We consider a game on a streak if the number after W or L is > 1

    # Extract the number part from the streak column
    df['Streak_Length'] = df['Streak'].str.extract(r'(\d+)').astype(int)

    # Count how many games have streak length > 1 (means continuation of previous result)
    streak_games = df[df['Streak_Length'] > 1].shape[0]
    print(team)
    print(f"Number of games on a streak: {streak_games}")

    # Percentage as well
    total_games = df.shape[0]
    print(f"Percentage of games on a streak: {streak_games / total_games * 100:.2f}%")
