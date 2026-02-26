import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

house = pd.read_csv("california_housing_test.csv")
# print(house)

# 1. zpusob
fig = plt.figure()
ax = plt.axes()
ax.scatter(house['latitude'], house['households'], s = 40, alpha = 0.5, c = "red", edgecolors= "b")

# 2. zpusob
fig = plt.figure()
ax = fig.add_subplot(121)
ax.scatter(house['latitude'], house['households'], s = 40, alpha = 0.5, c = "red", edgecolors= "b")
ax = fig.add_subplot(122)
ax.scatter(house['median_income'], house['households'], s = 40, alpha = 0.5, c = "red", edgecolors= "b")

# 3D graf
fig = plt.figure()
ax = plt.axes(projection = "3d")
ax.scatter(house['latitude'], house['households'], house["population"],s = 50, alpha = 0.5, c = "red", edgecolors= "b")

# 4D plot
fig = plt.figure()
ax = plt.axes(projection = "3d")
ax.scatter(house['latitude'], house['households'], house["population"],s = house["total_bedrooms"], alpha = 0.5, c = "red", edgecolors= "b")
ax.set_xlabel("Lattitude")
ax.set_ylabel("Household")


# 5D plot 
house = house.assign(evaluation=lambda df: (df['total_bedrooms'] > 500).astype(int))
# house = house.assign(evaluation=lambda df: df['total_bedrooms'].apply(lambda x: "good" if x > 500 else "poor"))
fig = plt.figure()
ax = plt.axes(projection="3d")

# Map evaluation to color: 1 → black, 0 → red
colors = house['evaluation'].map({0: "red", 1: "black"})

ax.scatter(
    house['latitude'], 
    house['households'], 
    house['population'], 
    s=house['total_bedrooms']/5, 
    alpha=0.5, 
    c=colors, 
    edgecolors="b"
)

ax.set_xlabel("Latitude")
ax.set_ylabel("Household")
ax.set_zlabel("Population")
plt.show()

