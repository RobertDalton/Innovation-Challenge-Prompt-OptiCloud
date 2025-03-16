from fastapi import HTTPException
from src.services.prompt_shield_service import PromptShieldService
from src.services.content_safety_service import ContentSafetyService

prompt_shield_service = PromptShieldService()
content_safety_service = ContentSafetyService()

class PromptPreprocessingController:
    @staticmethod
    def preprocess_prompt(user_prompt: str, documents: list = []):
        if not user_prompt:
            raise HTTPException(status_code=400, detail="userPrompt is required")

        # Step 1: Check for dangerous content with Content Safety
        safety_analysis = content_safety_service.analyze_content(user_prompt)
        if "error" in safety_analysis:
            raise HTTPException(status_code=500, detail="Error in Content Safety Service")

        if safety_analysis.get("blocked", False):
            raise HTTPException(status_code=403, detail="Prompt blocked due to content safety issues")

        # Step 2: Apply Prompt Shield
        shielded_prompt = prompt_shield_service.shield_prompt(user_prompt, documents)
        if "error" in shielded_prompt:
            raise HTTPException(status_code=500, detail="Error in Prompt Shield Service")

        return {"sanitized_prompt": shielded_prompt}
