import cv2
import serial
import threading
import speech_recognition_module  # Имя второго файла без .py
from time import sleep

# Подключение к Arduino через последовательный порт
arduino = serial.Serial('/dev/cu.usbserial-120', 9600)

# Отправка угла в Arduino
def send_angle_to_arduino(angle):
    arduino.write(f"{angle}\n".encode())  # Отправляем угол в Arduino

def run_face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Не удалось открыть камеру. Убедитесь, что она подключена.")
        exit()

    current_angle = 90  # Начальное положение сервопривода
    target_angle = 90   # Желаемое положение сервопривода
    face_detected = False
    angle_step = 2       # Максимальная скорость изменения угла

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Не удалось получить кадр.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                face_detected = True
                x, y, w, h = faces[0]  # Берем первое обнаруженное лицо
                face_center_x = x + w // 2
                frame_center_x = frame.shape[1] // 2

                # Плавное движение сервопривода в зависимости от положения лица
                angle_delta_x = face_center_x - frame_center_x

                if abs(angle_delta_x) > 30:
                    target_angle += angle_delta_x // 10  # Изменение желаемого угла
                    target_angle = max(0, min(180, target_angle))  # Ограничиваем угол от 0 до 180

            else:
                if face_detected:
                    face_detected = False
                    target_angle = 90  # Возвращаем в центр, если лицо исчезло

            # Постепенно изменяем текущий угол до целевого
            if current_angle < target_angle:
                current_angle = min(current_angle + angle_step, target_angle)
            elif current_angle > target_angle:
                current_angle = max(current_angle - angle_step, target_angle)

            # Отправляем текущий угол на Arduino только при изменении
            send_angle_to_arduino(current_angle)

            # Отображаем лицо на экране
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # При завершении программы возвращаем сервопривод в "прямое" положение
        send_angle_to_arduino(90)
        arduino.write("STOP\n".encode())
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    threading.Thread(target=speech_recognition_module.main).start()
    run_face_detection()
