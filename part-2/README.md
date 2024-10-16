# Project: Braves Pitching Stats Analysis (2018)

This project involves two Python scripts to interact with the MLB **StatsAPI** and an SQLite database of pitch-by-pitch data for the Atlanta Braves (2018 season). The first script pulls pitching data from the StatsAPI and saves it into a CSV file. The second script compares the data from the StatsAPI with local data from an SQLite database to calculate stat differences.

## Prerequisites

1. **Python 3.x** must be installed.
2. Install the required Python packages by running:

   ```bash
   pip install requests pandas sqlite3
   ```

---

## 1. **Script 1**: `fetch_api_data.py`

This script pulls relevant pitching stats for the **2018 Atlanta Braves** from the **StatsAPI** and stores them in a CSV file.

### How to Run

1. **Download or copy the script**: `fetch_api_data.py`
2. **Run the script** using Python:

   ```bash
   python fetch_api_data.py
   ```

3. The output will be saved in a file named `braves_2018_pitching_stats.csv`.

### What the Script Does

- Fetches pitching data for the 2018 Atlanta Braves from the MLB StatsAPI.
- Extracts relevant stats such as player ID, name, games played, wins, losses, strikeouts, walks, innings pitched, hits, home runs, earned runs, ERA, WHIP, and saves.
- Saves this data in a CSV file (`braves_2018_pitching_stats.csv`).

---

## 2. **Script 2**: `compare_api_vs_db.py`

This script compares stats from the StatsAPI and an SQLite database (`main.db`) that contains detailed pitch-by-pitch data for the 2018 Atlanta Braves. It calculates differences in key pitching stats like strikeouts, walks, innings pitched, hits, and home runs.

### How to Run

1. **Ensure you have an SQLite database** named `main.db` containing a `PITCHBYPITCH` table with columns such as `GameDate`, `PitcherID`, `IS_STRIKEOUT`, `IS_OUT`, `IS_HIT`, `IS_HOMERUN`, `LAST_PITCH_OF_PA`, etc.
2. **Download or copy the script**: `compare_api_vs_db.py`
3. **Run the script** using Python:

   ```bash
   python compare_api_vs_db.py
   ```

4. The output will be two CSV files:
   - `player_api_stats.csv`: Contains player stats from the StatsAPI.
   - `comparison_stats.csv`: Shows differences between API stats and database stats.

### What the Script Does

- Fetches pitching data for the 2018 Atlanta Braves from the StatsAPI.
- Queries the SQLite database to extract the corresponding stats for each pitcher from the `PITCHBYPITCH` table.
- Compares stats such as strikeouts, walks, innings pitched, hits, and home runs between the API and the database.
- Saves the results in two CSV files: one with raw API stats and another showing the stat differences.

---

### Interesting Findings

This second script is my brief attempt at creating an audit system. There were a couple of things I had to work through when coding it:

1. **ID Mismatch**: The `PITCHBYPITCH` table in the SQLite database uses `PitcherID`, while the StatsAPI uses `playerID`. I had to normalize and map the two different IDs to ensure the data could be compared correctly. This required formatting and matching between the two systems.

2. **Missing Data**: Not all pitchers from the StatsAPI were present in the `PITCHBYPITCH` table. To address this, I filtered out players that only existed in one of the sources and focused the comparison on players who were in both datasets. This highlights a gap in the pitch-by-pitch data, where some players' stats may not be fully captured in the local database.

### Next Steps for Developing an Audit System

To enhance this system, the following next steps could be taken:

- **Add Robust Error Handling**: Ensure that missing or mismatched data is flagged, and include logging mechanisms to track which players are missing between the datasets. This could involve adding detailed error messages when mismatches are detected or when a player's data is incomplete.
- **Automate Data Validation**: Develop a comprehensive set of checks to automatically flag discrepancies between the API and local data. This could involve defining acceptable ranges of deviation for certain stats (e.g., small differences in innings pitched might be acceptable, but large differences would trigger a review).
- **Expand Coverage**: Include additional data points or seasons to make the comparison system more robust and validate data across multiple years, not just 2018. This could help identify long-term gaps in the local database.
- **Detailed Reporting**: Generate reports that detail the exact discrepancies in a human-readable format. This would allow the team to easily review differences and take corrective actions.

---
