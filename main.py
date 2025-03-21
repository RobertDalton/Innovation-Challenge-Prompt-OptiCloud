from fastapi import FastAPI
from routes.spectral_shield_route import router as spectral_shield_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Spectral Shield API",
    description="API to prevent toxic user prompts using spectogram ggwave encoding (Gibberlink).",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(spectral_shield_router, prefix="/api/spectral-shield", tags=["Spectral Shield"])

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)