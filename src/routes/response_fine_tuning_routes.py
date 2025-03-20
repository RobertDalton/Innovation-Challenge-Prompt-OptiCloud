from fastapi import APIRouter
from src.controllers.response_fine_tuning_controller import ResponseFineTuningController
from src.models.response_fine_tuning_model import ResponseFineTuningRequest, ResponseFineTuningResponse

router = APIRouter()
controller = ResponseFineTuningController()

@router.post("/prompt", response_model=ResponseFineTuningResponse)
async def analyze_text(request: ResponseFineTuningRequest):
    """Analyze text through the complete security pipeline."""
    return await controller.analyze_text(request.text)