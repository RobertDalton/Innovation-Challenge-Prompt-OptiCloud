from fastapi import APIRouter
from src.controllers.text_security_controller import TextSecurityController
from src.models.text_security_model import TextSecurityRequest, TextSecurityResponse

router = APIRouter()
controller = TextSecurityController()

@router.post("/analyze", response_model=TextSecurityResponse)
async def analyze_text(request: TextSecurityRequest):
    """Analyze text through the complete security pipeline."""
    return await controller.analyze_text(request.text)