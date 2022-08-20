import sys
import speech_recognition as sr
import gtts
from playsound import playsound
import os
import time


class SpeechTextEngine:

    def __init__(self, translator=None, speaking_lang="en", listen_lang="en-US",) -> None:
        '''
        description:
            it consist both `speech to text` and `text to speech` modules

        Inputs:
            translator = translator for the `speaking language (speaking_lang) to english`

            speaking_lang = "in what language for `text to speech` respond `respond in that language`"

            listen_lang = "in what language should `speech to text` listen"

        Ouputs: None
        '''
        # Wake up commands
        self.ACTIVATION_COMMAND = [
            "hey friday", "hi friday", "are you there friday", "friday",
            "turn on", "are you there"
        ]
        self.recognizer = sr.Recognizer()
        self.translator = translator
        self.listen_lang = listen_lang
        self.speaking_lang = speaking_lang

    def get_audio(self, phrase_time_limit=3):
        '''
        description: 
            it capture the audio from microphone and return the audio signals

        Inputs: 
            phrase_time_limit = it is the maximum number of seconds that this will allow a phrase to continue before stopping
                                and returning the part of the phrase processed before the time limit was reached


        Outputs: audio signals

        '''

        with sr.Microphone() as src:
            print("Say...........")
            audio = self.recognizer.listen(
                src, phrase_time_limit=phrase_time_limit)
            print("audio recognized")

        return audio

    def audio_to_text(self, audio, lang="en-US"):
        '''
        description: it convert audio to text and `return text`

        Inputs: lang = in which language you want to convert 

        Outputs: `recoginized text`

        '''

        text = ""

        try:
            text = self.recognizer.recognize_google(
                audio, language=lang).lower()

            print(f"\nrecognized text :- {text}")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("request error")

        return text

    def speech_recognition(self,  lang=None):  # required (mal -> eng)
        '''
        description: 
            it recoganize the audio and convert into text form and return it 

        Inputs: 
            lang = in what language you are speaking; if `None` select default `english` 

        Outputs: text

        '''
        # can manually change the listening language
        # by changing the lang parameter
        listen_lang = self.listen_lang if lang == None else lang

        audio = self.get_audio()
        text = self.audio_to_text(audio=audio, lang=listen_lang)

        if self.translator != None:
            text = self.translator.translate(text=text)  # english text

        text = str(text).lower()

        return text

    def wakeup(self):
        '''
        description: 
            recoginize wakeup command

        Inputs: None

        Outputs: 
                if the command is a wakeup command then:
                        return `True`
                 else 
                        return `False`

        '''

        if self.speech_recognition() in self.ACTIVATION_COMMAND:
            return True

        return False

    def speak(self, text: str, lang=None):
        '''
        description:
            convert text to audio and play the audio

        Inputs: 
            text = the text you want play

        Outputs: 
            return None
            `play the text in audio`

        '''

        try:
            # can manually change the speeking language
            speeking_lang = self.speaking_lang if lang == None else lang

            # english -> specified language
            if self.translator != None:
                text = self.translator.translate(text=text, reverse=True)

            tts = gtts.gTTS(text, lang=speeking_lang)
            temp = "./.temp.mp3"
            tts.save(temp)
            playsound(temp)
            os.remove(temp)
        except AssertionError:
            print("could not play sound")


#---------- Testing
if __name__ == "__main__":

    sys.path.append('../')
    from services.general_services.language_translate import LanguageTranslate

    languageTranslator = LanguageTranslate(lang_from="ta", lang_to="en")
    spr = SpeechTextEngine(translator=languageTranslator,
                           speaking_lang="ta", listen_lang="ta-IN")

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
