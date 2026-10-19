# %% Cell 1: Import Libraries & Load Data
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset (using direct URL so sample_data isn't required locally)
url = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"
df = pd.read_csv(url)

# Display first few rows
df.head()

# %% Cell 2: Prepare Coordinates & Simple Scatter Plot
xs = df["longitude"]
ys = df["latitude"]

plt.scatter(xs, ys)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Simple Scatter Plot')
plt.show()

# %% Cell 3: Advanced Scatter Plot with Colorbar and Size
plt.figure(figsize=(10, 8))
plt.scatter(
    xs, 
    ys, 
    c=df['median_house_value'], 
    s=df['population'] / 100, 
    cmap='viridis', 
    alpha=0.4
)
plt.colorbar(label='Median House Value')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('California Housing: Median House Value and Population Density')
plt.show()