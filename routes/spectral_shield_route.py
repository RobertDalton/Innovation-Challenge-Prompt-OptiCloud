from fastapi import APIRouter
from controllers.spectral_shield_controller import SpectralShieldController
from models.spectral_shield_model import SpectralShieldRequest,SpectralShieldResponse

router = APIRouter()
controller = SpectralShieldController()

@router.post("/spectral_shield", response_model=SpectralShieldResponse)
async def spectral_prediction(request: SpectralShieldRequest):
    return await controller.spectral_prediction(request.text)