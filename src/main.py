from fastapi import FastAPI
from src.routes.content_safety_routes import router
from src.routes.language_detection_routes import router
from src.routes.content_safety_routes import router as content_safety_router
from src.routes.prompt_shield_routes import router as prompt_shield_router
from src.routes.language_detection_routes import router as language_detection_router

app = FastAPI(
    title="Content Safety API",
    description="API to analyze and shield text using Azure Content Safety",
    version="1.0"
)

# Include routes
app.include_router(content_safety_router, prefix="/api/content-safety", tags=["Content Safety"])
app.include_router(prompt_shield_router, prefix="/api/prompt-shield", tags=["Prompt Shield"])
app.include_router(language_detection_router, prefix="/api/language-detection", tags=["Language Detection"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
