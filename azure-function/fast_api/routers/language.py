from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

router = APIRouter()


class Prompt(BaseModel):
    file: str
    content: str
    language: str

response = []

@router.get("/language")
async def language():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        
        # Analyze each text file in the reviews folder
        reviews_folder = './static/reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            response.append(Prompt(file=file_name,content=text,language=detectedLanguage.primary_language.name))
        return response


    except Exception as ex:
        print(ex)