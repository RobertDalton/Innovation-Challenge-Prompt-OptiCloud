from pydantic import BaseModel

class AnalyzeTextRequest(BaseModel):
    text: str

class AnalyzeTextResponse(BaseModel):
    hate_severity: int
    self_harm_severity: int
    sexual_severity: int
    violence_severity: int
