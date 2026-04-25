import pandas as pd

df = pd.read_csv("exercices\\module 4\\Csv\\exercices\module 4\Csv\\fictitious_basketball_league_players_1200_v2 - fictitious_basketball_league_players_1200_v2.csv")
df["total_points"] = df["ppg"] * df["games"]
df["cost_per_point"] = df["salary"] / df["total_points"]
print(df.sort_values("cost_per_point", ascending=False).head(5))