import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# 串口配置
SERIAL_PORT = "COM4"  # Windows: "COM3" | Linux/macOS: "/dev/ttyUSB0"
BAUD_RATE = 9600  # 串口波特率

# 初始化串口
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
time.sleep(2)  # 等待串口稳定

# 初始数据（单个像素块）
data = np.array([[0]])  # 1x1 数组，存储压力数据

# 创建 Matplotlib 图像
fig, ax = plt.subplots(figsize=(2, 2))  # 画布大小适配单个色块
heatmap = ax.imshow(data, cmap="hot", vmin=0, vmax=1023)  # 颜色范围 0-1023

# 移除坐标轴刻度
ax.set_xticks([])
ax.set_yticks([])
plt.title("Pressure Indicator")

# **更新色块颜色**
def update_color(frame):    
    if ser.in_waiting > 0:
        try:
            sensor_value = int(ser.readline().decode("utf-8").strip())  # 读取数据
            data[0, 0] = sensor_value  # 更新单个像素值
            heatmap.set_data(data)  # 更新颜色
            heatmap.set_clim(vmin=0, vmax=1023)  # 确保颜色映射正确
        except ValueError:
            pass  # 过滤异常数据

    return [heatmap]

# 动画更新（实时刷新）
ani = animation.FuncAnimation(fig, update_color, interval=1, blit=True)

plt.colorbar(heatmap)  # 颜色条
plt.show()

# 关闭串口
ser.close()
