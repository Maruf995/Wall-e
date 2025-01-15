import cv2
import threading
import speech_recognition_module  # Имя второго файла без .py
from gpiozero import Servo
from time import sleep

# Параметры сервопривода
servo = Servo(17)  # Замените 17 на ваш GPIO-пин
servo_angle = 0  # Текущий угол сервопривода (от -1 до 1)

# Преобразование угла в диапазоне 0-180 в значение для gpiozero (-1 до 1)
def angle_to_position(angle):
    return angle / 90 - 1

# Устанавливаем начальное положение в центре (90 градусов)
servo.value = angle_to_position(90)

def run_face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

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

            frame_center_x = frame.shape[1] // 2
            if face_center_x < frame_center_x - 30:  # Лицо слева
                if current_angle > 0:
                    current_angle -= 5  # Поворачиваем влево
                    current_angle = max(0, current_angle)
                    servo.value = angle_to_position(current_angle)
            elif face_center_x > frame_center_x + 30:  # Лицо справа
                if current_angle < 180:
                    current_angle += 5  # Поворачиваем вправо
                    current_angle = min(180, current_angle)
                    servo.value = angle_to_position(current_angle)
        else:
            if face_detected:
                face_detected = False
                current_angle = 90  # Возвращаем в центр
                servo.value = angle_to_position(current_angle)

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
