import serial
import time

# Настройки последовательного порта
SERIAL_PORT = '/dev/cu.usbserial-120'  # Укажите ваш порт (например, COM3 для Windows)
BAUD_RATE = 9600

# Создаём подключение к последовательному порту
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Даем Arduino время на инициализацию

def rotate_servo(arduino, pin):
    """Поворот сервопривода."""
    try:
        arduino.write(f"ROTATE_{pin}\n".encode())
        time.sleep(1)
        arduino.write(f"CENTER_{pin}\n".encode())
        print(f"Серво на пине {pin} повернулся!")
    except Exception as e:
        print(f"Ошибка управления серво: {e}")


def main():
    for i in range(3):
        if arduino:
            time.sleep(3)
            rotate_servo(arduino, 9)

if __name__ == "__main__":
    main()