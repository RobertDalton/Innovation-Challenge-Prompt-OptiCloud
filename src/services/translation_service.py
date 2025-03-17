import os
import asyncio
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text import TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TranslationService:
    def __init__(self):
        self.key = os.getenv("TRANSLATION_KEY")
        self.endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
        self.region = os.getenv("TRANSLATION_REGION")
        self.source_language = "es"
        if not self.key or not self.endpoint:
            raise ValueError("Azure Translation Service credentials are missing.")
        self.credential = TranslatorCredential(self.key,self.region)

    async def translate_text(self, text: str):
        """Translate text to english using Translation Service."""
        if not self.source_language=="en":
            with TextTranslationClient(endpoint=self.endpoint, credential=self.credential) as client:
                try:
                    target_languages = ["en"]
                    input_text_elements = [InputTextItem(text=text)]
                    response = client.translate(content = input_text_elements, to = target_languages, from_parameter = self.source_language)
                    return self._parse_response(response)
                except HttpResponseError as e:
                    return {"error": str(e)}

    def _parse_response(self, response):
        """Parse tranlate from the response."""
        translation = response[0] if response else None
        if translation:
            for translated_text in translation.translations:
                return {
                    "translation": translated_text.text
                }
