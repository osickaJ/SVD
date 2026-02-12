import pandas as pd

df = pd.read_csv("penguins.csv")
#print(df)
df.info()

myDf = pd.DataFrame({"col1": [1,2,3], "col2": [4,5,6]}, ["row1", "row2", "row3"])
print(myDf)
print(myDf.describe())

myDf1 = pd.DataFrame({"morning": ["SAV","SDS","SSR"], "afternoon": ["TAI","MS","SVD"]}, ["po", "ut", "ct"])
print(myDf1)
a = myDf1.loc["ut", "morning"]
print(a)

print(df["island"].unique())
large_fem_peng = df[(df["body_mass_g"] > 4358) & (df["sex"] == "FEMALE")]
print(large_fem_peng)
print(len(large_fem_peng))

avg_mass = df.groupby("sex")["body_mass_g"].mean()
print(avg_mass)

# How much heavier males are on average
heavier = avg_mass["MALE"] - avg_mass["FEMALE"]
print(f"Males are on average {heavier:.1f} g heavier than females.")