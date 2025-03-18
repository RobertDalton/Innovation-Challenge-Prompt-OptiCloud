from pydantic import BaseModel
from typing import Dict, Any, Optional

class TextSecurityRequest(BaseModel):
    text: str

class TextSecurityResponse(BaseModel):
    safe: bool
    original_language: Optional[str] = None
    translated: bool = False
    content_safety_results: Dict[str, Any]
    prompt_shield_results: Dict[str, Any]
    error: Optional[str] = None