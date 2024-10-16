# Project: Braves Pitching Stats Analysis (2018)

This project involves two Python scripts to interact with the MLB **StatsAPI** and an SQLite database of pitch-by-pitch data for the Atlanta Braves (2018 season). The first script pulls pitching data from the StatsAPI and saves it into a CSV file. The second script compares the data from the StatsAPI with local data from an SQLite database to calculate stat differences.

## Prerequisites

**Python 3.x** must be installed. 2. Install the required Python packages by running:

```bash
pip install requests pandas sqlite3

```

Script 1: fetch_api_data.py
This script pulls relevant pitching stats for the 2018 Atlanta Braves from the StatsAPI and stores them in a CSV file.

How to Run
Download or copy the script: fetch_api_data.py

Run the script using Python:

python fetch_api_data.py
The output will be saved in a file named braves_2018_pitching_stats.csv.

What the Script Does
Fetches pitching data for the 2018 Atlanta Braves from the MLB StatsAPI.
Extracts relevant stats such as player ID, name, games played, wins, losses, strikeouts, walks, innings pitched, hits, home runs, earned runs, ERA, WHIP, and saves.
Saves this data in a CSV file (braves_2018_pitching_stats.csv).

Script 2: compare_api_vs_db.py
This second script is my brief attempt at creating an audit system. There were a couple things I had to workout when coding it up. Firstly the pitchbypitch db uses PitcherID while the api uses playerID, so I had to do some formatting between the two to get the comparisons working. Secondly I noticed that not all of the pitcher data is in the pitchbypitch table. Therefore I had to filter out which players existed in both.

The script basically compares stats from the StatsAPI and an SQLite database (main.db) that contains detailed pitch-by-pitch data for the 2018 Atlanta Braves. It calculates differences in key pitching stats like strikeouts, walks, innings pitched, hits, and home runs.

How to Run
Ensure you have an SQLite database named main.db containing a PITCHBYPITCH table with columns such as GameDate, PitcherID, IS_STRIKEOUT, IS_OUT, IS_HIT, IS_HOMERUN, LAST_PITCH_OF_PA, etc.

Download or copy the script: compare_api_vs_db.py

Run the script using Python:
python compare_api_vs_db.py
The output will be two CSV files:

player_api_stats.csv: Contains player stats from the StatsAPI.
comparison_stats.csv: Shows differences between API stats and database stats.
What the Script Does
Fetches pitching data for the 2018 Atlanta Braves from the StatsAPI.
Queries the SQLite database to extract the corresponding stats for each pitcher from the PITCHBYPITCH table.
Compares stats such as strikeouts, walks, innings pitched, hits, and home runs between the API and the database.
Saves the results in two CSV files: one with raw API stats and another showing the stat differences.
