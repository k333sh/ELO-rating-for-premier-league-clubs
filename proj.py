import pandas as pd
import glob as gb
import math
import matplotlib.pyplot as plt

from pandas.core.computation.ops import MathCall

files = gb.glob("rawData/*.csv")

print(files)

dfs = []

for f in files:
    print("Reading:", f)
    df = pd.read_csv(
        f,
        engine="python",
        on_bad_lines="skip",
        encoding="latin1"  # or encoding="cp1252"
    )
    dfs.append(df)

matches = pd.concat(dfs, ignore_index=True)

# print("Total matches:", len(matches))

matches["Date"] = pd.to_datetime(matches["Date"], format="%d/%m/%Y", errors="coerce")

matches = matches.dropna(subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"])
# print(matches[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].isna().sum())


matches = matches.sort_values("Date").reset_index(drop=True)
print(matches.head())
print(matches.isna().sum())

elo = {}
teams = pd.concat([matches["HomeTeam"], matches["AwayTeam"]]).unique()
for t in teams:
    elo[t] = 1500

history = []
for i, row in matches.iterrows():
    home = row["HomeTeam"]
    away = row["AwayTeam"]
    hg = row["FTHG"]
    ag = row["FTAG"]

    # Expected scores
    homeRating = elo[home]
    awayRating = elo[away]

    deltaR = homeRating - awayRating  # Quality diff
    MaxHomeAdvantageComponent = 55
    HomeWinProbability = 0.457
    scale = 1 + (deltaR / 4000)  # a scale that takes into account difference in quality
    H = (MaxHomeAdvantageComponent * scale)

    # Apply home advantage
    home_adj = homeRating + H
    away_adj = awayRating

    exp_home = 1 / (1 + 10 ** ((away_adj - home_adj) / 400))
    exp_away = 1 - exp_home

    if hg > ag:
        s_home, s_away = 1, 0
    elif hg < ag:
        s_home, s_away = 0, 1
    else:
        s_home, s_away = 0.5, 0.5
    # Dynamic K factor
    baseK = 30
    goalDiff = abs(hg - ag)
    if goalDiff == 0:
        K = baseK
    else:
        K = baseK * math.log(goalDiff + 1)

    elo[home] += K * (s_home - exp_home)
    elo[away] += K * (s_away - exp_away)

    history.append({"Date": row["Date"], "Team": home, "ELO": elo[home]})
    history.append({"Date": row["Date"], "Team": away, "ELO": elo[away]})

history_df = pd.DataFrame(history)



print("Top 15:")
for team, rating in sorted(elo.items(), key=lambda x: -x[1])[:15]:
    print(team, round(rating, 1))

print("\nBottom 15:")
for team, rating in sorted(elo.items(), key=lambda x: x[1])[:15]:
    print(team, round(rating, 1))


plt.style.use("dark_background")

# Teams and their updated colors
teams_colors = {
    "Man City": "#6CABDD",   # light blue
    "Tottenham": "#FFFFFF",         # white
    "Arsenal": "#F6BE00",           # gold
    "Man United": "#FF6A00", # orange
    "Liverpool": "#C8102E",         # dark red
    "Chelsea": "#034694"            # blue
}

plt.figure(figsize=(14,7))

for team, color in teams_colors.items():
    df_t = history_df[history_df["Team"] == team]
    if len(df_t) == 0:
        print(f"Warning: No data found for {team}")
        continue
    plt.plot(df_t["Date"], df_t["ELO"], label=team, color=color, linewidth=2)

plt.title("Premier League ELO Ratings Over Time (Selected Clubs)")
plt.xlabel("Date")
plt.ylabel("ELO Rating")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()



