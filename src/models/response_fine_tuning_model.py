from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union

class ResponseFineTuningRequest(BaseModel):
    text: str = Field(..., description="Input text to be analyzed")

class ResponseFineTuningResponse(BaseModel):
    prompt: Optional[str] = Field(None, description="Generated prompt (only if text is safe)")
    is_unsafe: Optional[Dict[str, Any]] = Field(None, description="Details if the text is unsafe")
