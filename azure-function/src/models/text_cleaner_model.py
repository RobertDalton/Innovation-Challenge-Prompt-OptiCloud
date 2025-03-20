from pydantic import BaseModel, Field
from typing import Optional

class TextCleanRequest(BaseModel):
    text: str = Field(
        ...,
        description="The input text to be cleaned",
        examples=["Hello! <script>alert('XSS')</script>"]
    )

class TextCleanResponse(BaseModel):
    original_text: str = Field(..., description="The original input text")
    cleaned_text: str = Field(..., description="The sanitized output text")
    characters_removed: int = Field(..., description="Number of characters removed during cleaning")
    error: Optional[str] = Field(None, description="Error message if cleaning failed")