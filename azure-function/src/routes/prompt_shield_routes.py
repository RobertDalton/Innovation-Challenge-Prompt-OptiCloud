from fastapi import APIRouter
from src.controllers.prompt_shield_controller import PromptShieldController
from src.models.prompt_shield_model import PromptShieldRequest, PromptShieldResponse

router = APIRouter()
controller = PromptShieldController()

@router.post("/shield-prompt", response_model=PromptShieldResponse)
def shield_prompt(request: PromptShieldRequest):
    """Shield a prompt against potential harmful content."""
    return controller.shield_prompt(request.user_prompt, request.documents)