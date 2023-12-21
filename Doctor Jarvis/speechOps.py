import os

import speech_recognition as sr

from gtts import gTTS

from typing import Any


class Transcribe:
    def __init__(self, language: str):
        self.language=language
        # initialise recogniser
        self.recognizer = sr.Recognizer()
        # initialise microphone
        self.mic = sr.Microphone()
    
    def get_text(self) -> Any:
        """
        convert audio from microphone to text 
        """

        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source=source)
            audio = self.recognizer.listen(source=source)
            transcribe = self.recognizer.recognize_google(audio_data=audio, 
                                                          language=self.language
                                                          )
            return transcribe


class Translate:
    def __init__(self, txt_msg: str, language: str):
        self.txt_msg = txt_msg
        self.language = language
    
    def text_to_speech(self):
        """
        using Google Text to Speech module, 
        recite a text in a given language
        """

        # name of audio file
        audio_file = os.path.join(os.getcwd(), 
                                  f"{os.getenv('audio_file')}.mp3"
                                  )
        # generate audio using module
        speech = gTTS(self.txt_msg, lang=self.language)
        # save to .mp3 file
        speech.save(audio_file)
        # play mp3 file
        os.system(command=f"mpg321 {audio_file}")
