import pandas as pd
import numpy as np

# 定义测量点（每 1cm 一个，共 10 个）
positions = np.arange(0.5, 10, 1)  # [0.5, 1.5, 2.5, ..., 9.5]

# 生成线性变化的电阻数据
resistance_1 = np.linspace(30, 60, len(positions))  # 30Ω 到 60Ω 线性变化
resistance_2 = np.linspace(30, 60, len(positions))  # 30Ω 到 60Ω 线性变化

# 随机生成压力数据（这里使用 1~5kPa 的随机数）
pressure = np.random.uniform(1, 5, len(positions))

# 创建 DataFrame
df = pd.DataFrame({
    "位置": positions,
    "电阻1": resistance_1,
    "电阻2": resistance_2,
    "压力": pressure
})

# 保存为 Excel 文件
df.to_excel("pressure_data.xlsx", index=False)

print("Excel 文件 'pressure_data.xlsx' 生成成功！")
