from fastapi import HTTPException
from services.spectral_shield_service import SpectralShieldService

class SpectralShieldController:
    def __init__(self):
        self.service = SpectralShieldService()

    async def spectral_prediction(self, text: str):
        """Calls the Spectral Shield Service and handles errors."""
        result = self.service.predict(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result