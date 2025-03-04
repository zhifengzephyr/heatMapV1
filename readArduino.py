import serial
import time

# 修改为你的 Arduino 端口，例如 "COM3" (Windows) 或 "/dev/ttyUSB0" (Linux/macOS)
SERIAL_PORT = "COM4"  # Windows: "COM3", "COM4" 等
BAUD_RATE = 9600  # 和 Arduino 代码中的 Serial.begin(9600) 保持一致

def read_arduino():
    try:
        # 连接串口
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # 等待 Arduino 复位
        print(f"Connected to {SERIAL_PORT}")

        while True:
            if ser.in_waiting > 0:  # 检查是否有数据
                data = ser.readline().decode("utf-8").strip()  # 读取数据并去除空格/换行
                print(f"Received: {data}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()  # 关闭串口

if __name__ == "__main__":
    read_arduino()
