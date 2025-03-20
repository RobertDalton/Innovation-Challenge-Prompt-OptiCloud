from pydantic import BaseModel

class SpectralShieldRequest(BaseModel):
    text: str

class SpectralShieldResponse(BaseModel):
    toxic: float
    safe: float
    audio_url: str
    spectogram_url: str
