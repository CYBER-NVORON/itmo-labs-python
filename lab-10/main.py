from requests import get
import pyttsx3
from pyaudio import PyAudio, paInt16
from vosk import Model, KaldiRecognizer
import json

""""
Сайт https://loripsum.net/api/10/short/headers
Примеры команд: "создать", "прочесть" (прочесть текст),
"сохранить" (сохранить как html),
"текст" (сохранить как текст без форматирования).
"""


class VoiceAssistant():

    def __init__(self):
        self.commands = [
            {"id": 0, "text": "создать",
             "answer": "Создан текст", "handler": self.create},
            {"id": 1, "text": "прочесть",
             "answer": "Читаю текст", "handler": self.read},
            {"id": 2, "text": "сохранить",
             "answer": "Файл сохранён", "handler": self.html_save},
            {"id": 3, "text": "текст",
             "answer": "Текст сохранён", "handler": self.txt_save},
            {"id": 4, "text": "закрыть",
             "answer": "Закрытие голосового ассистента!", "handler": quit}
        ]
        self.data = None

        self.tts = pyttsx3.init()
        self.model = Model('vosk-model-small-ru-0.22')
        self.record = KaldiRecognizer(self.model, 16000)
        pa = PyAudio()
        self.stream = pa.open(format=paInt16,
                              channels=1,
                              rate=16000,
                              input=True,
                              frames_per_buffer=8000)
        self.stream.start_stream()
        self.speak("Вас приветствует голосовой ассистент.")
        self.speak("Вот мои команды:")
        for command in self.commands:
            print(f"{command['id']+1}. \"{command['text']}\"")

    def create(self):
        self.data = get("https://loripsum.net/api/10/short/headers")

    def read(self):
        self.speak(self.data.text)

    def html_save(self):
        with open("download.html", "wb") as html_file:
            html_file.write(self.data.content)

    def txt_save(self):
        with open("text.txt", "w") as txt_file:
            txt_file.write(self.data.text)

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    print("Вы:", answer['text'])
                    yield answer['text']

    def speak(self, say):
        self.stream.stop_stream()
        print(say)
        self.tts.say(say)
        self.tts.runAndWait()
        self.stream.start_stream()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.speak('Начинаю работу')

    for text in assistant.listen():
        for command in assistant.commands:
            if text.startswith(command["text"]):
                if (assistant.data and command["id"] in [1, 2, 3]) or \
                        command["id"] in [0, 4]:
                    assistant.speak(command["answer"])
                    command["handler"]()
                else:
                    assistant.speak("Нет текста, используйте для начала команду \"Создать\"")
                break
        else:
            assistant.speak("Я не знаю этой команды!")
