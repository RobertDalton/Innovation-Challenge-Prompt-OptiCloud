from fastapi import HTTPException
from src.services.prompt_shield_service import PromptShieldService
from src.models.prompt_shield_model import PromptShieldResponse, UserPromptAnalysis, DocumentAnalysis

class PromptShieldController:
    def __init__(self):
        self.service = PromptShieldService()

    def shield_prompt(self, user_prompt: str, documents: list = None) -> PromptShieldResponse:
        """Shield a prompt using the PromptShield Service."""
        result = self.service.shield_prompt(user_prompt, documents)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return PromptShieldResponse(
            userPromptAnalysis=UserPromptAnalysis(
                attackDetected=result["userPromptAnalysis"]["attackDetected"]
            ),
            documentsAnalysis=[
                DocumentAnalysis(attackDetected=doc["attackDetected"]) 
                for doc in result.get("documentsAnalysis", [])
            ]
        )