import os
import time

import speech_recognition as sr

from gtts import gTTS
from pygame import mixer


class Transcribe:
    def __init__(self, language: str):
        self.language=language
        # initialise recogniser
        self.recognizer = sr.Recognizer()
        # initialise microphone
        self.mic = sr.Microphone()
    
    def get_text(self):
        """
        convert audio from microphone to text 
        """

        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source=source)
                audio = self.recognizer.listen(source=source)
                transcribed_txt = self.recognizer.recognize_google(
                    audio_data=audio, 
                    language=self.language
                )
                print(transcribed_txt)
                return transcribed_txt
        except sr.RequestError:
            return "NO INTERNET CONNECTION"


class Translate:
    def __init__(self, txt_msg: str, language: str):
        self.txt_msg = txt_msg
        self.language = language
        self.mixer = mixer.init()
    
    def text_to_speech(self):
        """
        using Google Text to Speech module, 
        recite a text in a given language
        """

        # name of audio file
        audio_file = os.path.join(
            os.getcwd(), 
            f"{os.getenv('audio_file')}.mp3"
        )
        # generate audio using module
        speech = gTTS(text=self.txt_msg, lang=self.language)
        # save to .mp3 file
        speech.save(savefile=audio_file)
        # play the mp3 file
        self.mixer.music.load(audio_file)
        self.mixer.music.play()
        # wait for music to finish playing
        while self.mixer.music.get_busy():
            time.sleep(secs=1)
