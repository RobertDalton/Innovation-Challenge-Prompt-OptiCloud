from fastapi import HTTPException
from src.services.content_safety_service import ContentSafetyService

class ContentSafetyController:
    def __init__(self):
        self.service = ContentSafetyService()

    async def analyze_text(self, text: str):
        """Calls the Content Safety Service and handles errors."""
        result = await self.service.analyze_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
