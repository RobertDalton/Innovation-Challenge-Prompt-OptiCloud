import azure.functions as func
from azurefunctions.extensions.http.fastapi import Request, StreamingResponse
from pydantic import BaseModel
import openai
import json
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
# Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

endpoint = os.getenv("AZURE_OPEN_AI_ENDPOINT")
api_key = os.getenv("AZURE_OPEN_AI_API_KEY")

# Azure Open AI
deployment = os.getenv("AZURE_OPEN_AI_DEPLOYMENT_MODEL")
temperature = 0.7

client = openai.AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2023-09-01-preview"
)

# Pydantic models for request and response
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    prompt: str

# Get data from Azure Open AI
async def stream_processor(response):
    async for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
                await asyncio.sleep(0)

# Get data from Azure Open AI
async def prompt_processor(response):
    full_response = ""
    async for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                full_response += delta.content
    yield PromptResponse(prompt=full_response).json()

# HTTP streaming Azure Function
@app.route(route="generate-text", methods=[func.HttpMethod.POST])
async def stream_openai_text(req: Request) -> StreamingResponse:
    try:
        # Validar el JSON de la solicitud con Pydantic
        req_body = await req.json()
        prompt_request = PromptRequest(**req_body)
        
        # Llamada al modelo de OpenAI con una instrucción clara sobre su rol
        system_prompt = "Tu rol es mejorar los prompts que recibes para hacerlos más claros, concisos y efectivos.Devuelve únicamente el prompt mejorado."
        azure_open_ai_response = await client.chat.completions.create(
            model=deployment,
            temperature=temperature,
            max_tokens=1000,
            messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_request.prompt}
                ],
            stream=True
        )

        return StreamingResponse(stream_processor(azure_open_ai_response), media_type="text/event-stream")
    except Exception as e:
        return StreamingResponse(json.dumps({"error": str(e)}), status_code=500, media_type="application/json")

@app.route(route="generate-prompt", methods=[func.HttpMethod.POST])
async def generate_text(req: Request) -> StreamingResponse:
    try:
        # Validar el JSON de la solicitud con Pydantic
        req_body = await req.json()
        prompt_request = PromptRequest(**req_body)
        
        # Llamada al modelo de OpenAI con una instrucción clara sobre su rol
        system_prompt = "Tu rol es mejorar los prompts que recibes para hacerlos más claros, concisos y efectivos. Devuelve únicamente el prompt mejorado."
        azure_open_ai_response = await client.chat.completions.create(
            model=deployment,
            temperature=temperature,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_request.prompt}
            ],
            stream=True
        )
        
        return StreamingResponse(prompt_processor(azure_open_ai_response), media_type="application/json")
    except Exception as e:
        return StreamingResponse(json.dumps({"error": str(e)}), status_code=500, media_type="application/json")