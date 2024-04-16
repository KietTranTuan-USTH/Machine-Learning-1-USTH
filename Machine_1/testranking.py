import pandas as pd

ranking = pd.read_csv("fifa_ranking-2023-07-20.csv",parse_dates=["rank_date"])
print(ranking.head())