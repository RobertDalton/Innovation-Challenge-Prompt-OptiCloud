from pydantic import BaseModel
from typing import List, Optional

class UserPromptAnalysis(BaseModel):
    attackDetected: bool

class DocumentAnalysis(BaseModel):
    attackDetected: bool

class PromptShieldRequest(BaseModel):
    user_prompt: str
    documents: Optional[List[str]] = []

class PromptShieldResponse(BaseModel):
    userPromptAnalysis: UserPromptAnalysis
    documentsAnalysis: Optional[List[DocumentAnalysis]] = []