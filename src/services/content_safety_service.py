import os
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

class ContentSafetyService:
    def __init__(self):
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    async def analyze_text(self, text: str):
        """Analyze text for harmful content."""
        request = AnalyzeTextOptions(text=text)

        async with self.client:
            try:
                response = await self.client.analyze_text(request)
            except HttpResponseError as e:
                print(f"Analyze text failed: {e}")
                return None

        result = {
            "hate": None,
            "self_harm": None,
            "sexual": None,
            "violence": None
        }

        for category_analysis in response.categories_analysis:
            if category_analysis.category == TextCategory.HATE:
                result["hate"] = category_analysis.severity
            elif category_analysis.category == TextCategory.SELF_HARM:
                result["self_harm"] = category_analysis.severity
            elif category_analysis.category == TextCategory.SEXUAL:
                result["sexual"] = category_analysis.severity
            elif category_analysis.category == TextCategory.VIOLENCE:
                result["violence"] = category_analysis.severity

        return result
