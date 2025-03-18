from fastapi import HTTPException
from src.services.pii_recognition_service import PIIRecognitionService
from src.models.pii_recognition_model import PIIRecognitionResponse

class PIIRecognitionController:
    def __init__(self):
        self.service = PIIRecognitionService()

    async def analyze_text(self, text: str) -> PIIRecognitionResponse:
        """Analyze text for PII using the PII Recognition Service."""
        result = await self.service.analyze_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return PIIRecognitionResponse(**result)