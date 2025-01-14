import cv2
import threading
import speech_recognition_module  # Имя второго файла без .py

def run_face_detection():
    # Загружаем предобученный классификатор для лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Открываем доступ к веб-камере
    cap = cv2.VideoCapture(0)

    # Проверяем, удалось ли открыть камеру
    if not cap.isOpened():
        print("Не удалось открыть камеру. Убедитесь, что она подключена.")
        exit()

    # Основной цикл для обработки кадров
    while True:
        # Считываем кадр с камеры
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break

        # Преобразуем кадр в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Обнаруживаем лица на кадре
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Рисуем прямоугольники вокруг найденных лиц
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Показываем обработанное видео
        cv2.imshow('Face Detection', frame)

        # Нажмите 'q', чтобы выйти
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Создаем поток для распознавания речи
    threading.Thread(target=speech_recognition_module.main).start()
    # Запускаем обнаружение лиц
    run_face_detection()
