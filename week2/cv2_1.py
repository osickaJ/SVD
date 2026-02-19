import numpy as np
import pandas as pd

df = pd.read_csv("dataset_vina.csv")
print(df.head())

print(df.isna().sum())

df["cukernatost"]  = df["cukernatost"].fillna(df["cukernatost"].median())
df["cena"] = df["cena"].fillna(df["cena"].mean())
print(df.isna().sum())


 # average price by year
df.groupby("ročník")["cena"].mean()

df.groupby("ročník")["cena"].mean().plot(kind = "pie")