import pandas as pd

df = pd.read_csv("exercices\module 4\Csv\fictitious_basketball_league_players_1200_v2 - fictitious_basketball_league_players_1200_v2.csv")
print(df.groupby("position")["salary"].agg(["mean", "max", "min"]))