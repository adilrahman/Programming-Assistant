from services.general_services.language_translate import LanguageTranslate
from speech_recognition_engine.speech_recognition_engine import SpeechTextEngine

speaking_lang = "ta"
listen_lang = "ta-IN"

languageTranslator = LanguageTranslate(lang_from="ta", lang_to="en")

speechTextClient = SpeechTextEngine(
    translator=languageTranslator, speaking_lang=speaking_lang, listen_lang=listen_lang)
