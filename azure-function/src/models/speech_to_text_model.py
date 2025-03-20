from pydantic import BaseModel

class SpeechTextResponse(BaseModel):
    prompt: str
