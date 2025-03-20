from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class TextSecurityRequest(BaseModel):
    text: str = Field(..., description="Input text to be analyzed")

class TextSecurityResponse(BaseModel):
    safe: bool = Field(..., description="Overall safety status of the text")
    original_language: Optional[str] = Field(None, description="Detected source language")
    translated: bool = Field(False, description="Whether text was translated")
    cleaned_text: str = Field(..., description="Text after sanitization")
    characters_removed: int = Field(0, description="Number of unsafe characters removed")
    pii_detected: bool = Field(False, description="Whether PII was found and redacted")
    pii_results: Dict[str, Any] = Field(..., description="Details of PII analysis")
    content_safety_results: Dict[str, Any] = Field(..., description="Content safety analysis results")
    prompt_shield_results: Dict[str, Any] = Field(..., description="Prompt injection analysis results")
    reason: Optional[str] = Field(None, description="Reason if text is unsafe")
    error: Optional[str] = Field(None, description="Error message if processing failed")