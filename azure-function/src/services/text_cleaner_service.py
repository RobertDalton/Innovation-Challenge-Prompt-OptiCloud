import re
from typing import Optional
from src.models.text_cleaner_model import TextCleanRequest, TextCleanResponse

class TextCleanerService:
    def __init__(self):
        # Regex pattern to keep only allowed characters
        self.pattern = r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ.,;!?¿¡(){}\[\]<>/*+=%-]'

    def clean_text(self, text: str) -> TextCleanResponse:
        """
        Removes unwanted characters from input text.
        """
        try:
            if not isinstance(text, str):
                raise ValueError("Input must be a string")
            
            cleaned_text = re.sub(self.pattern, '', text)
            chars_removed = len(text) - len(cleaned_text)
            
            return TextCleanResponse(
                original_text=text,
                cleaned_text=cleaned_text,
                characters_removed=chars_removed
            )
            
        except Exception as e:
            return TextCleanResponse(
                original_text=text,
                cleaned_text="",
                characters_removed=0,
                error=str(e)
            )