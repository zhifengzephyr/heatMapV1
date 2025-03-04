import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# 串口配置
SERIAL_PORT = "COM4"
BAUD_RATE = 9600

# 初始化串口
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)  # 缩短超时时间
time.sleep(2)

# 初始数据
data = np.array([[0]])

# 创建图像
fig, ax = plt.subplots(figsize=(2, 2))
heatmap = ax.imshow(data, cmap="hot", vmin=0, vmax=1023)
ax.set_xticks([])
ax.set_yticks([])
plt.title("Pressure Indicator")

def update_color(frame):
    raw_data = ser.read(ser.in_waiting)  # 非阻塞读取
    if raw_data:
        lines = raw_data.decode("utf-8", errors="ignore").split('\r\n')
        latest_value = data[0, 0]
        for line in lines:
            line = line.strip()
            if line:
                try:
                    latest_value = int(line)
                except ValueError:
                    pass
        data[0, 0] = latest_value
        heatmap.set_data(data)
        heatmap.set_clim(vmin=0, vmax=1023)
    return [heatmap]

# 动画参数优化
ani = animation.FuncAnimation(
    fig, 
    update_color, 
    interval=5, 
    blit=True,
    cache_frame_data=False
)

plt.colorbar(heatmap)
plt.show()

ser.close()