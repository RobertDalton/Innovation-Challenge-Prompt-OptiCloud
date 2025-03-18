from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PIIEntity(BaseModel):
    text: str
    category: str
    confidence_score: float
    offset: int
    length: int

class PIIRecognitionRequest(BaseModel):
    text: str

class PIIRecognitionResponse(BaseModel):
    redacted_text: Optional[str] = None
    entities: List[PIIEntity] = []
    error: Optional[str] = None