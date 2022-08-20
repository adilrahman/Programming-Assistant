import speech_recognition as sr
import gtts
from playsound import playsound
import os
import time
from services.general_services import LanguageTranslate

r = sr.Recognizer()

languageTranslate = LanguageTranslate(lang_from="ml", lang_to="en")
languageTranslate_1 = LanguageTranslate(lang_from="en", lang_to="ml")


class SpeechTextEngine:

    def __init__(self, speaking_lang="en", listen_lang="en-US") -> None:

        # Wake up commands
        self.ACTIVATION_COMMAND = [
            "hey friday", "hi friday", "are you there friday", "friday",
            "turn on", "are you there"
        ]

        self.listen_lang = listen_lang
        self.speaking_lang = speaking_lang

    def get_audio(self, phrase_time_limit=3):
        with sr.Microphone() as src:
            print("Say...........")
            audio = r.listen(src, phrase_time_limit=phrase_time_limit)
            print("audio recognized")

        return audio

    def audio_to_text(self, audio, lang="en-US"):
        text = ""

        try:
            text = r.recognize_google(audio, language=lang).lower()
            print(f"\nrecognized text :- {text}")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("request error")

        return text

    def speech_recognition(self,  lang="en-US"):
        audio = self.get_audio()
        text = self.audio_to_text(audio=audio, lang=self.listen_lang)
        text = languageTranslate.translate(text=text)
        text = str(text).lower()

        return text

    def wakeup(self):
        if self.speech_recognition() in self.ACTIVATION_COMMAND:
            return True
        return False

    def speak(self, text, lang="en"):
        try:
            text = languageTranslate_1.translate(text)
            tts = gtts.gTTS(text, lang=self.speaking_lang)
            temp = "./temp.mp3"
            tts.save(temp)
            playsound(temp)
            os.remove(temp)
        except AssertionError:
            print("could not play sound")


if __name__ == "__main__":

    spr = SpeechTextEngine()

    while True:
        if spr.wakeup():
            print("Activate")
            spr.speak("Activating")
            spr.speak("listening sir")
            time.sleep(1.5)
            while True:
                command = spr.speech_recognition()
                if "deactivate" in command:
                    print("Deactivate!")
                    spr.speak("Deactivating")
                    break
                else:
                    spr.speak("you said :- " + command)
