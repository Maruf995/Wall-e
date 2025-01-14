import openai
import pyttsx3
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

def main():
    recognizer = sr.Recognizer()
    tts = pyttsx3.init()

    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru') 
    tts.setProperty("rate", 150)
    tts.setProperty("volume", 1)

    for voice in voices:
        if voice.name == 'Aleksandr':
            tts.setProperty('voice', voice.id)

    while True:
        with sr.Microphone() as source:
            print("Скажите что-нибудь...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            continue
        except sr.RequestError as e:
            print(f"Ошибка сервиса; {e}")
            continue

        # Используйте ваш клиент OpenAI
        client = openai.OpenAI(
            api_key="6ac30328-5a39-4e77-931e-82e02f14f073",
            base_url="https://api.sambanova.ai/v1",
        )

        response = client.chat.completions.create(
            model='Meta-Llama-3.1-8B-Instruct',
            messages=[
                {"role": "system",
                 "content": "Your name is Валли! You are a robot exhibit at a science museum. You help children learn new things. But briefly."
                 },
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            top_p=0.1
        )

        answer = response.choices[0].message.content
        print(answer)
        tts = gTTS(text=answer, lang='ru', slow=False)
        tts.save("output.mp3")
        playsound("output.mp3")

if __name__ == "__main__":
    main()
