import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

# 串口配置
SERIAL_PORT = "COM4"  # Windows: "COM3", "COM4" 等
BAUD_RATE = 9600  # 和 Arduino 代码保持一致
UPDATE_INTERVAL = 5  # 更新间隔（ms）

# 连接 Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # 等待 Arduino 复位

# 创建 10×1 的空白热图数据
heatmap_data = np.zeros((10, 1))

# 自定义颜色映射（300=蓝色，600=白色，1023=红色）
colors = [(0, "blue"), (300/1023, "blue"), (600/1023, "white"), (1, "red")]
custom_cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)

# 设置 Matplotlib 画布
fig, ax = plt.subplots()
cax = ax.imshow(heatmap_data, cmap=custom_cmap, vmin=0, vmax=1023)  # 设定颜色范围
fig.colorbar(cax)  # 添加颜色条
ax.set_xticks([])  # 移除 x 轴刻度
ax.set_yticks(range(10))  # 设定 y 轴刻度
ax.set_yticklabels(["A0"] + [""] * 8 + ["A1"])  # 只显示 A0 和 A1 标签

# 读取 Arduino 数据并更新热图
def update_heatmap(frame):
    global heatmap_data
    if ser.in_waiting > 0:
        try:
            # 读取 Arduino 数据
            data = ser.readline().decode("utf-8").strip()
            values = data.split(",")

            if len(values) == 2:  # 确保是 2 个数据
                a0 = int(values[0])  # A0 读取值
                a1 = int(values[1])  # A1 读取值

                # 生成 10 行的插值数据
                heatmap_data[:, 0] = np.linspace(a0, a1, 10)  # 线性插值

                # 刷新 imshow 数据
                cax.set_array(heatmap_data)

        except ValueError:
            print(f"Invalid data received: {data}")

    return cax,

# 创建动画，每 5ms 更新一次热图
ani = animation.FuncAnimation(fig, update_heatmap, interval=UPDATE_INTERVAL, blit=False)

plt.show()

# 关闭串口
ser.close()
