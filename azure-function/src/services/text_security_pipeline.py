from typing import Dict, Any, Optional
from src.services.content_safety_service import ContentSafetyService
from src.services.prompt_shield_service import PromptShieldService
from src.services.language_detection_service import LanguageDetectionService
from src.services.translation_service import TranslationService
from src.services.pii_recognition_service import PIIRecognitionService
from src.services.text_cleaner_service import TextCleanerService

class TextSecurityPipeline:
    def __init__(self):
        self.language_detector = LanguageDetectionService()
        self.translator = TranslationService()
        self.pii_detector = PIIRecognitionService()
        self.content_safety = ContentSafetyService()
        self.prompt_shield = PromptShieldService()
        self.text_cleaner = TextCleanerService()
        self.severity_threshold = 5

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            # Step 1: Clean text
            clean_result = self.text_cleaner.clean_text(text)
            if clean_result.error:
                return {"error": clean_result.error}
            
            working_text = clean_result.cleaned_text
            
            # Step 2: Language detection step
            language = await self.language_detector.analyze_text(working_text)
            translated = False

            # Step 3: Translation step
            if language['iso6391_name'] != 'en':
                translation_result = await self.translator.translate_text(working_text)
                working_text = translation_result['translation']
                translated = True

            # Step 4: Check for PII
            pii_result = await self.pii_detector.analyze_text(working_text)
            if "error" in pii_result:
                return {"error": pii_result["error"]}

            # Use redacted text for further analysis if PII was found
            if pii_result.get("entities"):
                working_text = pii_result.get("redacted_text", working_text)

            # Step 5: Check content safety
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

            # Step 6: Check prompt shield
            shield_result = self.prompt_shield.shield_prompt(working_text)
            
            if "error" in shield_result:
                return {"error": shield_result["error"]}

            prompt_safe = (
                not shield_result["userPromptAnalysis"]["attackDetected"] and
                all(not doc["attackDetected"] for doc in shield_result.get("documentsAnalysis", []))
            )

            # Step 7: Return response
            return {
                "safe": prompt_safe,
                "translated": translated,
                "cleaned_text": clean_result.cleaned_text,
                "characters_removed": clean_result.characters_removed,
                "pii_detected": bool(pii_result.get("entities")),
                "pii_results": pii_result,
                "content_safety_results": safety_result,
                "prompt_shield_results": shield_result
            }

        except Exception as e:
            return {"error": f"Pipeline failed: {str(e)}"}