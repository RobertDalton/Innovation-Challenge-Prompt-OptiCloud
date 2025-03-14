import requests
import json
from src.config.azure_config import AZURE_ENDPOINT, AZURE_SUBSCRIPTION_KEY

class PromptShieldService:
    def __init__(self):
        self.endpoint = f"{AZURE_ENDPOINT}/contentsafety/text:shieldPrompt?api-version=2024-09-01"
        self.headers = {
            "Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }

    def shield_prompt(self, user_prompt: str, documents: list = []):
        try:
            payload = json.dumps({"userPrompt": user_prompt, "documents": documents})
            response = requests.post(self.endpoint, headers=self.headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error in Prompt Shield: {e}")
            return {"error": "Prompt Shield service failed"}
