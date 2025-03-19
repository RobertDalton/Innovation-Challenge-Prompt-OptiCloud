from fastapi import HTTPException
from src.services.text_cleaner_service import TextCleanerService
from src.models.text_cleaner_model import TextCleanResponse

class TextCleanerController:
    def __init__(self):
        self.service = TextCleanerService()

    async def clean_text(self, text: str) -> TextCleanResponse:
        result = self.service.clean_text(text)
        if result.error:
            raise HTTPException(status_code=500, detail=result.error)
        return result