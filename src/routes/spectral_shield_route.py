from fastapi import APIRouter
from src.controllers.spectral_shield_controller import SpectralShieldController
from src.models.spectral_shield_model import SpectralShieldRequest,SpectralShieldResponse

router = APIRouter()
controller = SpectralShieldController()

@router.post("/spectral_shield", response_model=SpectralShieldResponse)
async def spectral_prediction(request: SpectralShieldRequest):
    return await controller.spectral_prediction(request.text)