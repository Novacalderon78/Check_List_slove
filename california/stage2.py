import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. อ่านไฟล์ housing.csv ที่อยู่ในโฟลเดอร์เดียวกัน
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'california_housing_test.csv')

# หรือใช้แบบง่าย (หากรัน Terminal จากโฟลเดอร์ california):
# file_path = 'housing.csv'

df = pd.read_csv(file_path)

# 2. ตั้งค่าขนาดรูปภาพ
fig, ax = plt.subplots(figsize=(12, 9))

# 3. วาด Scatter plot
scatter = ax.scatter(
    df['longitude'], 
    df['latitude'],
    c=df['median_house_value'], 
    cmap='viridis', 
    s=df['population'] / 100, 
    alpha=0.6,
    edgecolors='none'
)

# 4. เพิ่มแถบสี (Colorbar)
cbar = fig.colorbar(scatter, ax=ax, label='Median House Value ($)')
cbar.ax.yaxis.label.set_size(12)

# 5. กำหนดชื่อกราฟ แกน และเส้นตาราง
ax.set_title('California Housing Density and Values\nPiyapong Intajinda CE6921', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)

# 6. จัดการระยะขอบและแสดงผล
plt.tight_layout()
plt.show()
plt.close()