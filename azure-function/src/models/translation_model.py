from pydantic import BaseModel

class TranslationTextRequest(BaseModel):
    text: str

class TranslationTextResponse(BaseModel):
    translation: str
