from fastapi import APIRouter
from src.controllers.content_safety_controller import ContentSafetyController
from src.models.content_safety_model import AnalyzeTextRequest, AnalyzeTextResponse

router = APIRouter()
controller = ContentSafetyController()

@router.post("/analyze-text", response_model=AnalyzeTextResponse)
async def analyze_text(request: AnalyzeTextRequest):
    return await controller.analyze_text(request.text)
