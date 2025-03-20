from fastapi import HTTPException
from src.services.response_fine_tuning_service import ResponseFineTuningService
from src.models.response_fine_tuning_model import ResponseFineTuningResponse

class ResponseFineTuningController:
    def __init__(self):
        self.service = ResponseFineTuningService()

    async def analyze_text(self, text: str) -> ResponseFineTuningResponse:
        result = await self.service.analyze_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return ResponseFineTuningResponse(**result)