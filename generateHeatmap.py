import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 Excel 文件
data = pd.read_excel("pressure_data.xlsx")

# 确保数据格式正确
print(data.head())

# 计算压力（如果 Excel 已经包含“压力”列，可以跳过这一步）
data['Calculated Pressure'] = data['电阻1'] * 0.1 + data['电阻2'] * 0.2  # 示例公式

# 创建热力图数据
heatmap_data = data.pivot(index='位置', columns='Calculated Pressure', values='压力')

# 绘制热力图
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='hot', annot=True)
plt.title('Pressure Distribution Heatmap')
plt.xlabel('Calculated Pressure')
plt.ylabel('Position (cm)')
plt.show()
