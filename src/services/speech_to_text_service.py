import os
import asyncio
import azure.cognitiveservices.speech as speech_sdk
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
from fastapi import HTTPException
from src.services.response_fine_tuning_service import ResponseFineTuningService
from src.services.translation_service import TranslationService
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
        self.model_response = ResponseFineTuningService()
        self.traslation_service = TranslationService()
        
    async def translate_text(self):
        """Translate text to english using Translation Service."""
        try:
            switch = "Repeat."
            while(switch == "Repeat."):
                """Language Recognition"""
                speak = self.speech_synthesizer.speak_text_async("Please start speaking for language recognition.").get()
                if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                    self.speech_synthesizer.speak_text_async("Error in voice synthesis. Please try again").get()
                    raise HTTPException(status_code=500, detail="Error in voice synthesis")
                language = self.speech_recognizer.recognize_once()
                auto_detect_source_language_result = speech_sdk.AutoDetectSourceLanguageResult(language)
                self.source_language = auto_detect_source_language_result.language
                text = await self.traslation_service.translate_text_target("Thank you! Your Language is "+self.languages[self.source_language]+".Now you can start, introduce your prompt",self.source_language[:2])
                self.speech_synthesizer.speak_text_async(text).get()
                self.translation_config.speech_recognition_language = self.source_language

                """Translation to english"""
                target_language = "en"
                translator = speech_sdk.translation.TranslationRecognizer(self.translation_config,audio_config=self.audio_config)
                result = translator.recognize_once_async().get()
                if result.reason != speech_sdk.ResultReason.TranslatedSpeech:
                    self.speech_synthesizer.speak_text_async("The audio could not be translated. Please try again").get()
                    raise HTTPException(status_code=500, detail="The audio could not be translated.")
                translation = result.translations[target_language]
                response = translation

                #Synthetized Text to Speech
                speech = result.translations[self.source_language[:2]]
                text = await self.traslation_service.translate_text_target("Your prompt is: ",self.source_language[:2])
                speak = self.speech_synthesizer.speak_text_async(text+speech).get()
                if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
                    self.speech_synthesizer.speak_text_async("Error in voice synthesis. Please try again").get()
                    raise HTTPException(status_code=500, detail="Error in voice synthesis")
                
                text = await self.traslation_service.translate_text_target("Please wait a moment. The prompt is being analyzed.",self.source_language[:2])

                self.speech_synthesizer.speak_text_async(text).get()
                prompt = await self.model_response.analyze_text(response)
                prompt_value = prompt.get("prompt", "No prompt available")
                if prompt_value == "Text is unsafe":
                    text = await self.traslation_service.translate_text_target("The prompt is insecure. It may contain sensitive information or an unacceptable request. Please review it and introduce another one. Then we could help you. Thank you.",self.source_language[:2])
                    self.speech_synthesizer.speak_text_async(text).get()
                else:
                    response = "Repeat."
                    while(response == "Repeat."):
                        text = await self.traslation_service.translate_text_target("The recommendation for the improvedprompt is: "+prompt_value,self.source_language[:2])
                        self.speech_synthesizer.speak_text_async(text).get()
                        text = await self.traslation_service.translate_text_target("Would you like the prompt to be repeated? Please answer repeat or stop.",self.source_language[:2])
                        self.speech_synthesizer.speak_text_async(text).get()
                        answer = translator.recognize_once_async().get()
                        translation = answer.translations[target_language]
                        response = translation
                        if(response != "Stop."):
                            response = "Repeat."
                        else:
                            text = await self.traslation_service.translate_text_target("Would you like to introduce other prompt? Please answer repeat or stop.",self.source_language[:2])
                            self.speech_synthesizer.speak_text_async(text).get()
                            answer = translator.recognize_once_async().get()
                            translation = answer.translations[target_language]
                            switch = translation
                            if(switch != "Stop."):
                                switch = "Repeat."
                            else:
                                switch = "Stop."
                            response = "Stop."
            return self._parse_response(prompt_value)
        
        except HttpResponseError as e:
            return {"error": str(e)}

    def _parse_response(self, response):
        """Parse response."""
        return {
            "prompt": response
        }
