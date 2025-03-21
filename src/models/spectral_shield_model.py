from pydantic import BaseModel

class SpectralShieldRequest(BaseModel):
    text: str

class SpectralShieldResponse(BaseModel):
    toxic: float
    safe: float
    decision: str
    audio_url: str
    spectogram_url: str
