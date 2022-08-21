from services.general_services.language_translate import LanguageTranslate
from speech_recognition_engine.speech_recognition_engine import SpeechTextEngine

# speaking and listening language config
speaking_lang = "en"
listen_lang = "en-US"

languageTranslator = LanguageTranslate(lang_from="ml", lang_to="en")

languageTranslator = None

# translator == None then it select default config (english)
speechTextClient = SpeechTextEngine(
    translator=languageTranslator, speaking_lang=speaking_lang, listen_lang=listen_lang)
