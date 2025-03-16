from fastapi import FastAPI
from src.routes.content_safety_routes import router

app = FastAPI(title="Content Safety API", description="API to analyze text using Azure Content Safety", version="1.0")

# Include routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
