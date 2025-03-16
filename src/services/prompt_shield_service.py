import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PromptShieldService:
    def __init__(self):
        self.key = os.getenv("CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
        if not self.key or not self.endpoint:
            raise ValueError("Azure Content Safety credentials are missing.")
        
        # Construct the shield prompt endpoint
        self.shield_endpoint = f"{self.endpoint}/contentsafety/text:shieldPrompt?api-version=2024-09-01"
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json"
        }

    def shield_prompt(self, user_prompt: str, documents: list = None):
        """Shield a prompt using Azure Content Safety API."""
        if documents is None:
            documents = []

        payload = {
            "userPrompt": user_prompt,
            "documents": documents
        }

        try:
            response = requests.post(
                self.shield_endpoint,
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Shield prompt failed: {response.text}"}
        except Exception as e:
            return {"error": f"Shield prompt service failed: {str(e)}"}
