from fastapi import APIRouter
from src.controllers.translation_controller import TranslationController
from src.models.translation_model import TranslationTextRequest, TranslationTextResponse

router = APIRouter()
controller = TranslationController()

@router.post("/translate", response_model=TranslationTextResponse)
async def analyze_text(request: TranslationTextRequest):
    return await controller.translate_text(request.text)
