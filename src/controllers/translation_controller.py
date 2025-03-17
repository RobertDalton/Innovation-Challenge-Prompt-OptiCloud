from fastapi import HTTPException
from src.services.translation_service import TranslationService

class TranslationController:
    def __init__(self):
        self.service = TranslationService()

    async def translate_text(self, text: str):
        """Calls the Translate Service and handles errors."""
        result = await self.service.translate_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
