import os

import playsound
import speech_recognition as sr

from gtts import gTTS


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

    def text_to_speech(self):
        """
        using Google Text to Speech module, 
        recite a text in a given language
        """

        filename = os.path.join(os.getcwd(), "voice.mp3")
        audio = gTTS(text=self.txt_msg, lang=self.language)
        audio.save(savefile=filename)
        playsound.playsound(sound=filename)
        os.rmdir(path=filename)        
