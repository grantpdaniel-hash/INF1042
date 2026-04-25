import pandas as pd

with pd.option_context(
    "display.max_rows", None,
    "display.max_columns", None,
    "display.width", None,
    "display.max_colwidth", None
):    
    #garder le code imbriqué ici
    # 1) Charger le CSV
    df = pd.read_csv("exercices\\module 4\\Csv\\fichier.csv")
    #...
    print(df)