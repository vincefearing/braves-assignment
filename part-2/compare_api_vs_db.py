import requests
import pandas as pd
import sqlite3

# Step 1: Fetch Data from StatsAPI
url = "https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&playerPool=all&season=2018&teamId=144"
response = requests.get(url)
data = response.json()

# Extract relevant data (player id, name, and more stats)
players_data = []
for player in data['stats'][0]['splits']:
    player_info = {
        'playerID': str(player['player']['id']).strip(),
        'name_api': player['player']['fullName'],
        'strikeouts_api': player['stat'].get('strikeOuts', 0),
        'walks_api': player['stat'].get('baseOnBalls', 0),
        'inningsPitched_api': player['stat'].get('inningsPitched', 0),
        'hits_api': player['stat'].get('hits', 0),
        'homeRuns_api': player['stat'].get('homeRuns', 0)
    }
    players_data.append(player_info)

# Step 2: Create a DataFrame for API stats
statsapi_df = pd.DataFrame(players_data)

# Step 3: Load the PITCHBYPITCH data from the SQLite database
db_path = 'main.db'  # Ensure this is the correct path to your SQLite database
conn = sqlite3.connect(db_path)

# Query to extract key stats from PITCHBYPITCH filtered by the correct date format for 2018
query = """
SELECT 
    PitcherID as playerID,
    PitcherName as name_db,
    SUM(CASE WHEN IS_STRIKEOUT = '1' THEN 1 ELSE 0 END) as strikeouts_db,
    SUM(CASE WHEN BALLS = '4' THEN 1 ELSE 0 END) as walks_db,
    SUM(CASE WHEN IS_OUT = '1' AND LAST_PITCH_OF_PA = '1' THEN 1 ELSE 0 END) / 3.0 as inningsPitched_db,  -- Calculate innings pitched based on outs
    SUM(CASE WHEN IS_HIT = '1' THEN 1 ELSE 0 END) as hits_db,
    SUM(CASE WHEN IS_HOMERUN = '1' THEN 1 ELSE 0 END) as homeRuns_db
FROM PITCHBYPITCH
WHERE GameDate LIKE '%/2018'
GROUP BY PitcherID, PitcherName;
"""

pbb_df = pd.read_sql_query(query, conn)
conn.close()

# Step 4: Merge the API and database stats on playerID
merged_df = pd.merge(statsapi_df, pbb_df, on='playerID', how='inner')

# Step 5: Calculate differences between API and DB stats
merged_df['strikeout_diff'] = merged_df['strikeouts_api'] - merged_df['strikeouts_db']
merged_df['walks_diff'] = merged_df['walks_api'] - merged_df['walks_db']
merged_df['innings_diff'] = merged_df['inningsPitched_api'].astype(float) - merged_df['inningsPitched_db'].astype(float)
merged_df['hits_diff'] = merged_df['hits_api'] - merged_df['hits_db']
merged_df['homeRuns_diff'] = merged_df['homeRuns_api'] - merged_df['homeRuns_db']

# Step 6: Save a CSV file with playerID, name_api, and all API stats
api_stats_csv = 'player_api_stats.csv'
merged_df[['playerID', 'name_api', 'strikeouts_api', 'walks_api', 'inningsPitched_api', 'hits_api', 'homeRuns_api']].to_csv(api_stats_csv, index=False)

# Step 7: Save a CSV file with comparison of stats (API vs DB)
comparison_csv = 'comparison_stats.csv'
merged_df[['playerID', 'name_api', 'strikeout_diff', 'walks_diff', 'innings_diff', 'hits_diff', 'homeRuns_diff']].to_csv(comparison_csv, index=False)

# Step 8: Print summary
print(f"Players found in both datasets: {len(merged_df)}")
print(f"API stats saved to {api_stats_csv}")
print(f"Comparison results saved to {comparison_csv}")
