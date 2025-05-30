#l bozo

import requests
import pandas as pd
import time

t = ["ANA", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "UTA", "VAN", "VEG", "WPG", "WSH"] 

for team in t[29:]:
    time.sleep(5)
    url = "https://www.hockey-reference.com/teams/" + team + "/2025_games.html"
    print(f"Fetching URL: {url}")

    response = requests.get(url)
    response.raise_for_status()

    tables = pd.read_html(response.text)
    print(f"Number of tables found: {len(tables)}")

    df = tables[0]

    df = df.rename(columns={
        'GP': 'Game',
        'Date': 'Date',
        'Time': 'Time',
        'Unnamed: 3': 'Home/Away',
        'Opponent': 'Opponent',
        'GF': 'Goals For',
        'GA': 'Goals Against',
        'Unnamed: 7': 'OT',
        'Unnamed: 8': 'Notes',
        'W': 'Wins',
        'L': 'Losses',
        'OL': 'Overtime Losses',
        'Streak': 'Streak',
        'Att.': 'Attendance',
        'LOG': 'Log',
        'Notes': 'Notes2'
    })

    df['Home/Away'] = df['Home/Away'].apply(lambda x: 'Away' if x == '@' else 'Home')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    numeric_cols = ['Game', 'Goals For', 'Goals Against', 'Wins', 'Losses', 'Overtime Losses', 'Attendance']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Export to CSV
    csv_filename = team + '_2025_games.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
