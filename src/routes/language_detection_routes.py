from fastapi import APIRouter
from src.controllers.language_detection_controller import LanguageDetectionController
from src.models.language_detection_model import AnalyzeTextRequest, AnalyzeTextResponse

router = APIRouter()
controller = LanguageDetectionController()

@router.post("/language-detection", response_model=AnalyzeTextResponse)
async def analyze_text(request: AnalyzeTextRequest):
    return await controller.analyze_text(request.text)
