from fastapi import HTTPException
from src.services.speech_to_text_service import SpeechService

class SpeechController:
    def __init__(self):
        self.service = SpeechService()

    async def translate_text(self):
        """Calls the Translate Service and handles errors."""
        result = await self.service.translate_text()
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
