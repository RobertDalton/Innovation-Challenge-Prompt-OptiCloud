from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.content_safety_routes import router as content_safety_router
from src.routes.prompt_shield_routes import router as prompt_shield_router
from src.routes.language_detection_routes import router as language_detection_router
from src.routes.translation_routes import router as translation_router
from src.routes.text_security_routes import router as text_security_router
from src.routes.pii_recognition_routes import router as pii_recognition_router
from src.routes.text_cleaner_routes import router as text_cleaner_router
from src.routes.speech_to_text_routes import router as speech_router
from src.routes.response_fine_tuning_routes import router as response_fine_tuning_router

app = FastAPI(
    title="Content Safety API",
    description="API to analyze and shield text using Azure Content Safety",
    version="1.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (cambiar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
