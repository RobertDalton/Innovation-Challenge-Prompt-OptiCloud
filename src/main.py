from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from src.routes.content_safety_routes import router as content_safety_router
from src.routes.prompt_shield_routes import router as prompt_shield_router
from src.routes.language_detection_routes import router as language_detection_router
from src.routes.translation_routes import router as translation_router
from src.routes.text_security_routes import router as text_security_router
from src.routes.pii_recognition_routes import router as pii_recognition_router
from src.routes.text_cleaner_routes import router as text_cleaner_router
from routes.spectral_shield_route import router as spectral_shield_router
from src.routes.speech_to_text_routes import router as speech_router
from src.routes.response_fine_tuning_routes import router as response_fine_tuning_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Content Safety API",
    description="API to analyze and secure text inputs using Azure Content Safety and Spectral Shield",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Include routes
app.include_router(content_safety_router, prefix="/api/content-safety", tags=["Content Safety"])
app.include_router(prompt_shield_router, prefix="/api/prompt-shield", tags=["Prompt Shield"])
app.include_router(language_detection_router, prefix="/api/language", tags=["Language Detection"])
app.include_router(translation_router, prefix="/api/language", tags=["Translation"])
app.include_router(text_security_router, prefix="/api/text-security", tags=["Text Security"])
app.include_router(pii_recognition_router, prefix="/api/pii", tags=["PII Recognition"])
app.include_router(text_cleaner_router, prefix="/api/text-cleaner", tags=["Text Cleaning"])
app.include_router(speech_router, prefix="/api/speech", tags=["Speech"])
app.include_router(response_fine_tuning_router, prefix="/api/request", tags=["Request Fine Tunning Model"])
app.include_router(spectral_shield_router, prefix="/api/spectral-shield", tags=["Spectral Prediction"])



# #testing

# # Definir un modelo de entrada para recibir un string
# class RequestModel(BaseModel):
#     text: str

# # Crear un router para la API de "Request Fine Tuning Model"
# response_fine_tuning_router = APIRouter()

# @response_fine_tuning_router.post("/testing")
# async def get_fine_tuning_response(request: RequestModel):
#     return {
#         "toxic": 0.72153,
#         "safe": 0.27847,
#         "audio_url": "https://res.cloudinary.com/de69sgtob/video/upload/v1742451362/spectral_fc833736-0524-40d8-956f-872d8c4610e2.wav.wav",
#         "spectogram_url": "https://res.cloudinary.com/de69sgtob/image/upload/v1742451364/spectral_5f595540-d321-46b3-a61c-aacc8ae67a40.png.png"
#     }

# # Incluir el router con el prefijo y los tags
# app.include_router(response_fine_tuning_router, prefix="/api/test", tags=["Request Fine Tuning Model"])
# #testing




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
