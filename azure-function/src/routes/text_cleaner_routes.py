from fastapi import APIRouter
from src.controllers.text_cleaner_controller import TextCleanerController
from src.models.text_cleaner_model import TextCleanRequest, TextCleanResponse

router = APIRouter()
controller = TextCleanerController()

@router.post("/clean", response_model=TextCleanResponse)
async def clean_text(request: TextCleanRequest):
    return await controller.clean_text(request.text)