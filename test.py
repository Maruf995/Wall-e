import serial
from time import sleep

arduino = serial.Serial('/dev/cu.usbserial-10', 9600)

while True:
    arduino.write(b'180\n')  # Отправить угол 90
    sleep(1)
    arduino.write(b'0\n')  # Отправить угол 90
    sleep(1)
