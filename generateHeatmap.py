import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 串口配置
SERIAL_PORT = "COM4"  # Windows: "COM3", "COM4" 等
BAUD_RATE = 9600  # 和 Arduino 代码保持一致


# 连接 Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # 等待 Arduino 复位

# 创建 2×1 的空白热图数据
heatmap_data = np.zeros((2, 1))

# 设置 Matplotlib 画布
fig, ax = plt.subplots()
cax = ax.imshow(heatmap_data, cmap="hot", vmin=0, vmax=1023)  # 设定颜色范围为 0~1023
fig.colorbar(cax)  # 添加颜色条
ax.set_xticks([])  # 移除 x 轴刻度
ax.set_yticks([0, 1])  # 设定 y 轴刻度
ax.set_yticklabels(["A0", "A1"])  # 设置 y 轴标签

# 读取 Arduino 数据并更新热图
def update_heatmap(frame):
    global heatmap_data
    if ser.in_waiting > 0:
        try:
            # 读取 Arduino 数据
            data = ser.readline().decode("utf-8").strip()
            values = data.split(",")

            if len(values) == 2:  # 确保是 2 个数据
                a0 = int(values[0])
                a1 = int(values[1])

                # 更新热图数据
                heatmap_data[0, 0] = a0
                heatmap_data[1, 0] = a1

                # 刷新 imshow 数据
                cax.set_array(heatmap_data)

        except ValueError:
            print(f"Invalid data received: {data}")

    return cax,

# 创建动画，调用 update_heatmap
ani = animation.FuncAnimation(fig, update_heatmap, interval=5, blit=False)

plt.show()

# 关闭串口
ser.close()
