from fastapi import APIRouter
from src.controllers.speech_to_text_controller import SpeechController
from src.models.speech_to_text_model import SpeechTextResponse

router = APIRouter()
controller = SpeechController()

@router.get("/speech-translate", response_model=SpeechTextResponse)
async def analyze_text():
    return await controller.translate_text()
