import requests
import pandas as pd

# Step 1: Fetch Data from StatsAPI
url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&playerPool=all&season=2018&teamId=144"
response = requests.get(url)
data = response.json()

# Step 2: Extract relevant data (player id, name, and more stats)
players_data = []
for player in data['stats'][0]['splits']:
    player_info = {
        'playerID': str(player['player']['id']).strip(),
        'name': player['player']['fullName'],
        'gamesPlayed': player['stat'].get('gamesPlayed', 0),
        'wins': player['stat'].get('wins', 0),
        'losses': player['stat'].get('losses', 0),
        'strikeouts': player['stat'].get('strikeOuts', 0),
        'walks': player['stat'].get('baseOnBalls', 0),
        'inningsPitched': player['stat'].get('inningsPitched', 0),
        'hits': player['stat'].get('hits', 0),
        'homeRuns': player['stat'].get('homeRuns', 0),
        'earnedRuns': player['stat'].get('earnedRuns', 0),
        'era': player['stat'].get('era', 0),
        'whip': player['stat'].get('whip', 0),
        'saves': player['stat'].get('saves', 0)
    }
    players_data.append(player_info)

# Step 3: Create a DataFrame for API stats
statsapi_df = pd.DataFrame(players_data)

# Step 4: Save the DataFrame to a CSV file
csv_filename = 'braves_2018_pitching_stats.csv'
statsapi_df.to_csv(csv_filename, index=False)

print(f"API stats saved to {csv_filename}")