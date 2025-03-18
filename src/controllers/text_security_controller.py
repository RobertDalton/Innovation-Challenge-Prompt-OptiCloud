from fastapi import HTTPException
from src.services.text_security_pipeline import TextSecurityPipeline
from src.models.text_security_model import TextSecurityResponse

class TextSecurityController:
    def __init__(self):
        self.pipeline = TextSecurityPipeline()

    async def analyze_text(self, text: str) -> TextSecurityResponse:
        result = await self.pipeline.analyze_text(text)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return TextSecurityResponse(**result)