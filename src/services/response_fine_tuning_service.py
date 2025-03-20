from typing import Dict, Any
import httpx
from src.services.text_security_pipeline import TextSecurityPipeline

class ResponseFineTuningService:
    def __init__(self):
        self.text_security = TextSecurityPipeline()

    async def fetch_prompt_from_api(self, text: str) -> str:
        """Función para obtener un prompt desde una API externa."""
        url = "https://opticloud-http-streaming.azurewebsites.net/generate-text"
        payload = {"prompt": text}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            return response.text

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            is_safe = True
            result = await self.text_security.analyze_text(text)

            # Validaciones de seguridad
            if not result.get("safe", True):  
                is_safe = False
            if result.get("pii_detected", False):
                is_safe = False
            if result.get("prompt_shield_results", {}).get("userPromptAnalysis", {}).get("attackDetected", False):
                is_safe = False

            if is_safe:
                prompt = await self.fetch_prompt_from_api(text)
                return {
                    "prompt": prompt,  
                    "is_unsafe": result
                }
            else:
                return {
                    "prompt": "Text is unsafe",
                    "is_unsafe": result
                }

        except Exception as e:
            return {"error": f"Pipeline failed: {str(e)}"}
