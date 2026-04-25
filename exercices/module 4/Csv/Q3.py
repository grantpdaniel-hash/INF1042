import pandas as pd

df = pd.read_csv("exercices\module 4\Csv\fictitious_basketball_league_players_1200_v2 - fictitious_basketball_league_players_1200_v2.csv")
low = df[df["ppg"] < 5]
low.to_csv("low_scorers.csv", index=False)