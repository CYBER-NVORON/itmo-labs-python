import requests

import pyttsx3, pyaudio, vosk #install py3-tts for mac helps
import platform 
import json, os
""""
Сайт https://loripsum.net/api/10/short/headers
Примеры команд: "создать", "прочесть" (прочесть текст),
"сохранить" (сохранить как html), "текст" (сохранить как текст без форматирования).
"""

class Voice_assistant():
    
    def __init__(self) -> None:

        if platform.system() == "Darwin":
            #Тестировалось только для mac
            self.tts = pyttsx3.init('nsss')
            self.voices = self.tts.getProperty('voices')
            self.tts.setProperty('voices', 'ru')
            for voice in self.voices:
                if voice.name == 'Milena':
                    self.tts.setProperty('voice', voice.id)
            self.model = vosk.Model(os.getcwd() + '/model_small') # Лучше использовать нормальную модель, но она дольше обрабатывается и много весит =(
            self.record = vosk.KaldiRecognizer(self.model, 16000)
            self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            self.stream.start_stream()

        else:
            #Не тестировалось
            self.tts = pyttsx3.init('sapi5')
            self.voices = self.tts.getProperty('voices')
            self.tts.setProperty('voices', 'en')
            for voice in self.voices:
                if voice.name == 'Microsoft Zira Desktop - English (United States)':
                    self.tts.setProperty('voice', voice.id)
            self.record = vosk.KaldiRecognizer(vosk.Model(os.getcwd() + '/model_small'), 16000)
            self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            self.stream.start_stream()

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


    def speak(self, say):
        print(say)
        self.tts.say(say)
        self.tts.runAndWait()

if __name__ == "__main__":
    va = Voice_assistant()

    gen_data = None
    va.speak('Начинаю работу')

    for text in va.listen():
        if text == 'закрыть':
            quit()
        elif text == 'создать':
            gen_data = requests.get("https://loripsum.net/api/10/short/headers")
            va.speak('Создан текст')
        
        elif text == 'прочесть':
            if gen_data:
                va.speak(gen_data.text)
            else:
                va.speak("Нет текста, используйте для начала команду \"Создать\"")

        elif text == 'сохранить':
            if gen_data:
                with open("download.html", "wb") as htmlFile:
                    htmlFile.write(gen_data.content)
                
                va.speak("Файл сохранён")
            else:
                va.speak("Нет текста, используйте для начала команду \"Создать\"")

        elif text == 'текст':
            if gen_data:
                with open("text.txt", "w") as txtFile:
                    txtFile.write(gen_data.text)
                
                va.speak("Текст сохранён")
            else:
                va.speak("Нет текста, используйте для начала команду \"Создать\"")
                
        else:
            va.speak('Я вас не поняла, повторите команду')