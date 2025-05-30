# note



import requests
import pandas as pd
from io import StringIO

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 200)        # Adjust width to prevent line wrapping

def scrape_all_nhl_teams_and_save(year=2025, filename="nhl_standings.csv"):
    url = f"https://www.hockey-reference.com/leagues/NHL_{year}.html"
    response = requests.get(url)
    response.raise_for_status()

    html_io = StringIO(response.text)
    tables = pd.read_html(html_io)

    east = tables[0]
    west = tables[1]

    east_clean = east[~east['Unnamed: 0'].str.contains('Division', na=False)].reset_index(drop=True)
    west_clean = west[~west['Unnamed: 0'].str.contains('Division', na=False)].reset_index(drop=True)

    all_teams = pd.concat([east_clean, west_clean], ignore_index=True)

    # Save to CSV
    all_teams.to_csv(filename, index=False)

    print(f"Saved {len(all_teams)} teams to {filename}")

if __name__ == "__main__":
    scrape_all_nhl_teams_and_save()