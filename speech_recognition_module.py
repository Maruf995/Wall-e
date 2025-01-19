import openai
import pyttsx3
import time
import serial
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr


def setup_tts():
    """Инициализация синтезатора речи."""
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty("rate", 150)
    tts.setProperty("volume", 1)

    for voice in voices:
        if voice.name == 'Aleksandr':
            tts.setProperty('voice', voice.id)
    return tts


def connect_to_arduino(port='/dev/cu.usbserial-120', baud_rate=9600):
    """Подключение к Arduino."""
    try:
        arduino = serial.Serial(port, baud_rate)
        time.sleep(2)  # Ожидание инициализации соединения
        return arduino
    except serial.SerialException as e:
        print(f"Ошибка подключения к Arduino: {e}")
        return None


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
    recognizer = sr.Recognizer()
    tts = setup_tts()

    arduino = connect_to_arduino()
    if not arduino:
        print("Не удалось подключиться к Arduino. Продолжение без управления серво.")
    
    while True:
        with sr.Microphone() as source:
            print("Скажите что-нибудь...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="ru-RU")
                print(f"Вы сказали: {text}")
            except sr.UnknownValueError:
                print("Не удалось распознать речь")
                continue
            except sr.RequestError as e:
                print(f"Ошибка сервиса; {e}")
                continue
            except sr.WaitTimeoutError:
                print("Время ожидания истекло.")
                continue

        # Проверка на приветствие
        if any(keyword in text for keyword in ('Хай Гитлер', 'Хайль Гитлер', 'Привет Валли', 'Привет Валь','Привет Валя','Привет ва', 'Привет вал', 'Привет')):
            print("Приветствие обнаружено!")
            if arduino:
                rotate_servo(arduino, 9)
            continue

        # Используйте ваш клиент OpenAI
        try:
            client = openai.OpenAI(
                api_key="6ac30328-5a39-4e77-931e-82e02f14f073",
                base_url="https://api.sambanova.ai/v1",
            )

            response = client.chat.completions.create(
                model='Meta-Llama-3.1-8B-Instruct',
                messages=[
                    {"role": "system",
                     "content": "Your name is Валли! You are a robot exhibit at a science museum. You help children learn new things. But briefly. "
                     },
                    {"role": "user", "content": text}
                ],
                temperature=0.1,
                top_p=0.1
            )

            answer = response.choices[0].message.content
            print(answer)
            tts = gTTS(text=answer, lang='ru', slow=False)
            tts.save("audio/output.mp3")
            playsound("audio/output.mp3")

        except Exception as e:
            print(f"Ошибка взаимодействия с OpenAI: {e}")


if __name__ == "__main__":
    main()