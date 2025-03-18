import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.exceptions import HttpResponseError
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PIIRecognitionService:
    def __init__(self):
        self.key = os.getenv("AI_SERVICE_KEY")
        self.endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        if not self.key or not self.endpoint:
            raise ValueError("Azure AI Service credentials are missing.")
        self.credential = AzureKeyCredential(self.key)

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for PII (Personally Identifiable Information).
        Args:
            text: The text to analyze
        Returns:
            Dict containing PII analysis results
        """
        with TextAnalyticsClient(self.endpoint, self.credential) as client:
            try:
                response = client.recognize_pii_entities([text], language="en")[0]
                return self._parse_response(response)
            except HttpResponseError as e:
                return {"error": str(e)}

    def _parse_response(self, response) -> Dict[str, Any]:
        """
        Parse the PII recognition response.
        Args:
            response: Raw response from Azure API
        Returns:
            Structured dictionary with PII information
        """
        if hasattr(response, 'is_error') and response.is_error:
            return {"error": "Failed to analyze text for PII"}

        entities = []
        for entity in response.entities:
            entities.append({
                "text": entity.text,
                "category": entity.category,
                "confidence_score": entity.confidence_score,
                "offset": entity.offset,
                "length": entity.length
            })

        return {
            "redacted_text": response.redacted_text,
            "entities": entities
        }