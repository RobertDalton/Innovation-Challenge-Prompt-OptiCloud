import os
import asyncio
import azure.cognitiveservices.speech as speech_sdk
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

class SpeechService:
    def __init__(self):
        self.key = os.getenv("SPEECH_KEY")
        self.region = os.getenv("SPEECH_REGION")
        self.source_language = "en-US"
        self.auto_detect_source_language_config = speech_sdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "es-ES","pt-PT","fr-FR"])
        if not self.key or not self.region:
            raise ValueError("Azure Translation Service credentials are missing.")
        self.speech_config = speech_sdk.SpeechConfig(self.key, self.region)
        self.audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config=self.speech_config, 
        auto_detect_source_language_config=self.auto_detect_source_language_config, 
        audio_config=self.audio_config)
        self.translation_config = speech_sdk.translation.SpeechTranslationConfig(self.key, self.region)
        self.translation_config.add_target_language('en')
        self.translation_config.add_target_language('fr')
        self.translation_config.add_target_language('es')
        self.translation_config.add_target_language('pt')
        # Available voices
        self.voices = {
            "en": "en-US-AlloyTurboMultilingualNeural",
            "es": "en-US-AlloyTurboMultilingualNeural",
            "fr": "en-US-AlloyTurboMultilingualNeural",
            "pt": "en-US-AlloyTurboMultilingualNeural"
        }
        self.speech_config.speech_synthesis_voice_name = self.voices.get("en")
        self.speech_synthesizer = speech_sdk.SpeechSynthesizer(self.speech_config)
        self.languages={"en-US":"English", 
                         "es-ES":"Spanish",
                         "pt-PT":"Portuguese",
                         "fr-FR":"French"}
        
    async def translate_text(self):
        """Translate text to english using Translation Service."""
        try:
            """Language Recognition"""
            self.speech_synthesizer.speak_text_async("Please start speaking for language recognition.").get()
            language = self.speech_recognizer.recognize_once()
            auto_detect_source_language_result = speech_sdk.AutoDetectSourceLanguageResult(language)
            self.source_language = auto_detect_source_language_result.language
            self.speech_synthesizer.speak_text_async("Thank you! Your Language is "+self.languages[self.source_language]+".Now you can start, introduce your prompt").get()
            self.translation_config.speech_recognition_language = self.source_language

            """Translation to english"""
            target_language = "en"
            translator = speech_sdk.translation.TranslationRecognizer(self.translation_config,audio_config=self.audio_config)
            result = translator.recognize_once_async().get()
            if result.reason != speech_sdk.ResultReason.TranslatedSpeech:
                self.speech_synthesizer.speak_text_async("The audio could not be translated.").get()
                raise HTTPException(status_code=500, detail="The audio could not be translated.")
            translation = result.translations[target_language]
            response = translation

            #Synthetized Text to Speech
            speech = result.translations[self.source_language[:2]]
            speak = self.speech_synthesizer.speak_text_async(speech).get()
            if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                self.speech_synthesizer.speak_text_async("Error in voice synthesis").get()
                raise HTTPException(status_code=500, detail="Error in voice synthesis")
            
            return self._parse_response(response)
        
        except HttpResponseError as e:
            return {"error": str(e)}

    def _parse_response(self, response):
        """Parse response."""
        return {
            "prompt": response
        }
