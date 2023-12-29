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
                return transcribed_txt
        except sr.RequestError:
            return "NO INTERNET CONNECTION"


class ToAudio:
    def __init__(self, language: str):
        self.language = language
        # audio file name
        self.audio_file = os.path.join(
            os.getcwd(), 
            os.getenv(key='AUDIO_FILE')
        )
        self.delete_file()
    
    def delete_file(self):
        """
        delete audio file
        """

        if os.path.exists(path=self.audio_file):
            with open(file=self.audio_file, mode='rb') as f:
                f.close()
            os.remove(path=self.audio_file)
    
    def text_to_speech(self, txt_msg: str):
        """
        using Google Text to Speech module, 
        recite a text in a given language

        Params:
            txt_msg (str): text message
        """
        
        audio = gTTS(text=txt_msg, lang=self.language)
        audio.save(savefile=self.audio_file)
        audio.timeout = 10
        audio.speed = 'slow'
        playsound.playsound(sound=self.audio_file)
        self.delete_file()   
