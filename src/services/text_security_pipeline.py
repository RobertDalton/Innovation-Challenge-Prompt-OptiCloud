from typing import Dict, Any, Optional
from src.services.content_safety_service import ContentSafetyService
from src.services.prompt_shield_service import PromptShieldService
from src.services.language_detection_service import LanguageDetectionService
from src.services.translation_service import TranslationService

class TextSecurityPipeline:
    def __init__(self):
        self.language_detector = LanguageDetectionService()
        self.translator = TranslationService()
        self.content_safety = ContentSafetyService()
        self.prompt_shield = PromptShieldService()
        self.severity_threshold = 5

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            # Step 1: Language detection step
            language = await self.language_detector.analyze_text(text)
            working_text = text
            translated = False

            # Step 2: Translation step
            if language['iso6391_name'] != 'en':
                working_text = await self.translator.translate_text(text)
                working_text = working_text['translation']
                translated = True

            # Step 3: Check content safety
            safety_result = await self.content_safety.analyze_text(working_text)
            
            if "error" in safety_result:
                return {"error": safety_result["error"]}

            content_safe = all(
                severity < self.severity_threshold 
                for severity in [
                    safety_result["hate_severity"],
                    safety_result["self_harm_severity"],
                    safety_result["sexual_severity"],
                    safety_result["violence_severity"]
                ]
            )

            if not content_safe:
                return {
                    "safe": False,
                    "reason": "Content safety check failed",
                    "details": safety_result
                }

            # Step 4: Check prompt shield
            shield_result = self.prompt_shield.shield_prompt(working_text)
            
            if "error" in shield_result:
                return {"error": shield_result["error"]}

            prompt_safe = (
                not shield_result["userPromptAnalysis"]["attackDetected"] and
                all(not doc["attackDetected"] for doc in shield_result.get("documentsAnalysis", []))
            )

            # Step 5: Return response
            return {
                "safe": prompt_safe,
                # "original_language": language,
                "translated": translated,
                "content_safety_results": safety_result,
                "prompt_shield_results": shield_result
            }

        except Exception as e:
            return {"error": f"Pipeline failed: {str(e)}"}