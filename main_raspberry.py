import cv2
import serial
import threading
import speech_recognition_module  # Имя второго файла без .py
from time import sleep

# Подключение к Arduino через последовательный порт
arduino = serial.Serial('/dev/cu.usbserial-10', 9600)

# Отправка угла в Arduino
def send_angle_to_arduino(angle):
    arduino.write(f"{angle}\n".encode())  # Отправляем угол в Arduino

def run_face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Не удалось открыть камеру. Убедитесь, что она подключена.")
        exit()

    current_angle = 90  # Начальное положение сервопривода
    face_detected = False

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
            face_center_y = y + h // 2

            frame_center_x = frame.shape[1] // 2
            frame_center_y = frame.shape[0] // 2

            # Плавное движение сервопривода в зависимости от положения лица
            angle_delta_x = face_center_x - frame_center_x
            angle_delta_y = face_center_y - frame_center_y

            # Угол на основе горизонтальной оси
            if abs(angle_delta_x) > 30:
                current_angle += angle_delta_x // 10  # Плавное изменение угла
                current_angle = max(0, min(180, current_angle))  # Ограничиваем угол от 0 до 180

            # Плавно отправляем угол на Arduino
            send_angle_to_arduino(current_angle)

        else:
            if face_detected:
                face_detected = False
                current_angle = 90  # Возвращаем в центр
                send_angle_to_arduino(current_angle)

        # Отображаем лицо на экране
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    threading.Thread(target=speech_recognition_module.main).start()
    run_face_detection()
