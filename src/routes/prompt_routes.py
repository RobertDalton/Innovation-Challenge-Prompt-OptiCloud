from fastapi import APIRouter
from pydantic import BaseModel
from src.controllers.prompt_preprocessing_controller import PromptPreprocessingController

router = APIRouter()

class PromptRequest(BaseModel):
    user_prompt: str
    documents: list = []

@router.post("/preprocess")
async def preprocess_prompt(request: PromptRequest):
    return PromptPreprocessingController.preprocess_prompt(request.user_prompt, request.documents)
