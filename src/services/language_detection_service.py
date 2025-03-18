import os
import asyncio
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LanguageDetectionService:
    def __init__(self):
        self.key = os.getenv("AI_SERVICE_KEY")
        self.endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        if not self.key or not self.endpoint:
            raise ValueError("Azure AI Service credentials are missing.")
        self.credential = AzureKeyCredential(self.key)

    async def analyze_text(self, text: str):
        """Analyze text for language detection using Ai Service API."""
        with TextAnalyticsClient(self.endpoint, self.credential) as client:
            try:
                response = client.detect_language(documents=[text])[0]
                return self._parse_response(response)
            except HttpResponseError as e:
                return {"error": str(e)}

    def _parse_response(self, response):
        """Extract language from the response."""
        return {
            "detected_language": response.primary_language.name,
            "iso6391_name": response.primary_language.iso6391_name
        }
