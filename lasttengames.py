import pandas as pd

# Function to extract result from a row
def get_result(row):
    return row["OT"]

def get_location(row):
    return row["Home/Away"]

# Get last 6 results before index i
def get_last_6_results(df, i):
    if i < 6:
        return None
    return df.loc[i-6:i-1].apply(get_result, axis=1).tolist()

# Calculate win percentage
def calculate_win_percentage(results):
    if not results:
        return None
    wins = results.count('W')
    return round(wins / len(results) * 100, 1)

t = ["ANA", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJS", "STL", "TBL", "TOR", "UTA", "VAN", "VEG", "WPG", "WSH"] 
poopteams = ["BOS", "BUF", "PHI", "SJS", "SEA", "CHI", "NSH"]
midteams = ["MTL", "DET", "NJD", "CBJ", "NYR", "NYI", "PIT", "ANA", "VAN", "UTA"]
goodteams = []
total1 = 0
total2 = 0
total3 = 0
total4 = 0
teams = []
homewins = 0
homelosses = 0
awaywins = 0
awaylosses = 0


for team in midteams:

    # Load your CSV file
    csv_filename = team + '_2025_games.csv'
    df = pd.read_csv(csv_filename)

    # Counters
    matches_trend = 0
    breaks_trend = 0
    neutral_win = 0
    neutral_loss = 0

    # Main loop
    for i in range(len(df)):
        
        current_result = get_result(df.loc[i])
        location = get_location(df.loc[i])
        last_6_results = get_last_6_results(df, i)
        if current_result == 'W' and location == "Home":
            homewins += 1
        elif current_result == 'L' and location == "Home":
            homelosses += 1
        elif current_result == 'L' and location == "Away":
            awaylosses += 1
        elif current_result == 'W' and location == "Away":
            awaywins += 1
        
        if last_6_results is not None:
            win_pct = calculate_win_percentage(last_6_results)
        

            if win_pct > 50:
                if current_result == 'W':
                    matches_trend += 1
                    print(f"Game {i+1}: Matches winning trend ✅")
                else:
                    breaks_trend += 1
                    print(f"Game {i+1}: Breaks winning trend ❌")

            elif win_pct < 50:
                if current_result != 'W':
                    matches_trend += 1
                    print(f"Game {i+1}: Matches losing trend ✅")
                else:
                    breaks_trend += 1
                    print(f"Game {i+1}: Breaks losing trend ❌")

            else:  # win_pct == 50
                if current_result == 'W':
                    neutral_win += 1
                    print(f"Game {i+1}: Neutral trend, win ⚪✅")
                else:
                    neutral_loss += 1
                    print(f"Game {i+1}: Neutral trend, loss ⚪❌")

    # Print final summary
    print("\n--- SUMMARY ---")
    print(f"Matched trend: {matches_trend}")
    print(f"Broke trend: {breaks_trend}")
    print(f"Neutral trend & win: {neutral_win}")
    print(f"Neutral trend & loss: {neutral_loss}")
    #if matches_trend == breaks_trend:
    teams.append(team)
    total1 += matches_trend
    total2 += breaks_trend
    total3 += neutral_win
    total4 += neutral_loss

print("\n--- TOTAL SUMMARY ---")
print(f"Matched trend: {total1}")
print(f"Broke trend: {total2}")
print(f"Neutral trend & win: {total3}")
print(f"Neutral trend & loss: {total4}")
print(teams)
print('homelosses')
print('homewins')
print('awaywins')
print('awaylosses')
print(homelosses)
print(homewins)
print(awaywins)
print(awaylosses)