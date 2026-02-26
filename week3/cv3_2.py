import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

population = np.random.rand(100)
area = np.random.randint(100,600,100)
kontinent = ["America", "Europe", "Asia", "Australia"]*25

df = pd.DataFrame(dict(population = population, area = area, kontinent = kontinent))
colors = {"America" : "red", "Europe" : "green", "Asia" : "yellow", "Australia" : "blue"}

plt.figure(figsize=(8,6))
plt.scatter(
    df['area'], 
    df['population'], 
    c=df['kontinent'].map(colors),  # map continent to color
    alpha=0.7,
    edgecolors='k'
)
plt.xlabel("Area")
plt.ylabel("Population")
plt.title("Population vs Area by Continent")
plt.show()
