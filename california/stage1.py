import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("california/california_housing_test.csv")

xs = df["longitude"]
ys = df["latitude"]
plt.figure(figsize=(10, 8))
plt.title('California Housing: Piyapong Intajinda CE6921')
plt.scatter(xs, ys)
plt.show()
print(xs)