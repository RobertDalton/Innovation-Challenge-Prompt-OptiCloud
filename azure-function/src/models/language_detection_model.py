from pydantic import BaseModel

class AnalyzeTextRequest(BaseModel):
    text: str

class AnalyzeTextResponse(BaseModel):
    detected_language: str
    iso6391_name: str
