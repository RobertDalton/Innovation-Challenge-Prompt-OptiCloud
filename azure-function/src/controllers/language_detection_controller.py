from fastapi import HTTPException
from src.services.language_detection_service import LanguageDetectionService

class LanguageDetectionController:
    def __init__(self):
        self.service = LanguageDetectionService()

    async def analyze_text(self, text: str):
        """Calls the Language Detection Service and handles errors."""
        result = await self.service.analyze_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
