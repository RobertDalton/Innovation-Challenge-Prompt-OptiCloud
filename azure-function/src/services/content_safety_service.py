import os
import asyncio
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ContentSafetyService:
    def __init__(self):
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        if not self.key or not self.endpoint:
            raise ValueError("Azure Content Safety credentials are missing.")
        self.credential = AzureKeyCredential(self.key)

    async def analyze_text(self, text: str):
        """Analyze text for harmful content using Azure Content Safety API."""
        async with ContentSafetyClient(self.endpoint, self.credential) as client:
            request = AnalyzeTextOptions(text=text)
            try:
                response = await client.analyze_text(request)
                return self._parse_response(response)
            except HttpResponseError as e:
                return {"error": str(e)}

    def _parse_response(self, response):
        """Extract severity levels from the response."""
        return {
            "hate_severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.HATE), 0),
            "self_harm_severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SELF_HARM), 0),
            "sexual_severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SEXUAL), 0),
            "violence_severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.VIOLENCE), 0),
        }
