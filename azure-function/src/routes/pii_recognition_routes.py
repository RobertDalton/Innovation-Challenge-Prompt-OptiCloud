from fastapi import APIRouter
from src.controllers.pii_recognition_controller import PIIRecognitionController
from src.models.pii_recognition_model import PIIRecognitionRequest, PIIRecognitionResponse

router = APIRouter()
controller = PIIRecognitionController()

@router.post("/analyze", response_model=PIIRecognitionResponse)
async def analyze_text(request: PIIRecognitionRequest):
    """Analyze text for PII (Personally Identifiable Information)."""
    return await controller.analyze_text(request.text)