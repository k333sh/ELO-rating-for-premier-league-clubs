# Premier League ELO Rating System (1999–2024)

A custom, data‑driven **ELO rating model** built on 25 years of Premier League match data.  
This project loads every match from 1999/00 to 2023/24, processes the results, applies a modernized ELO algorithm, and visualizes team strength over time.

This repo is designed as a **sports analytics portfolio piece**, showcasing data engineering, modeling, and visualization skills.

---

## Features

- **Full multi‑season data ingestion**  
  - Loads all CSV files from `rawData/`  
  - Cleans and merges them into a single chronological match dataset  
  - Handles encoding issues and malformed rows

- **Custom ELO rating engine**  
  - Dynamic, data‑driven home advantage based on historical home win rates  
  - Home advantage scaled by rating difference between teams  
  - Log‑scaled K‑factor that reacts to goal difference  
  - Continuous ratings across seasons (no reset)

- **Rating history tracking**  
  - After every match, updated ratings for both teams are stored  
  - Produces a `history` table with:
    - Date  
    - Team  
    - ELO rating  

- **Visualization**  
  - Dark‑mode matplotlib plots  
  - Color‑coded ELO trajectories for major clubs:
    - Manchester City  
    - Arsenal  
    - Liverpool  
    - Chelsea  
    - Manchester United  
    - Tottenham Hotspur  

---

## How the model works

1. **Data loading and cleaning**
   - Read all CSVs from `rawData/` using `glob`
   - Parse dates, drop invalid rows, and sort matches by date

2. **Initialization**
   - Each team starts at an ELO rating of **1500**

3. **Dynamic home advantage**
   - Base home advantage derived from historical home win probability (~45.7%)
   - Adjusted using rating differences

4. **Expected scores**
   - Uses the standard ELO logistic function on adjusted ratings (home rating + H)

5. **Rating updates**
   - Actual scores: 1 (win), 0.5 (draw), 0 (loss)
   - Dynamic K‑factor based on goal difference
   - New rating:
     
     


6. **History tracking**
   - After each match, store:
     - Date  
     - Team  
     - Updated ELO  
   - Converted into a `history` DataFrame for plotting

---

## Example visualizations

- ELO rating over time for a single club (e.g., Arsenal)
- Multi‑team comparison plot (Man City, Arsenal, Liverpool, Chelsea, Man United, Spurs)
- Dark background with club‑inspired colors:
  - Man City — light blue  
  - Arsenal — gold  
  - Liverpool — dark red  
  - Chelsea — blue  
  - Man United — orange  
  - Spurs — white  

---

## Tech stack

- **Python**
- **Pandas** – data cleaning and manipulation
- **Matplotlib** – visualization
- **Glob** – multi‑file ingestion
- **Math** – ELO calculations

---

## Project structure

```text
├── rawData/              # All CSV match files (1999–2024)
├── elo_model.py          # Main ELO engine and plotting code
└── README.md             # Project documentation
