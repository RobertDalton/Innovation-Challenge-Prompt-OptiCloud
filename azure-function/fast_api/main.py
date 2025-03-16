from fastapi import FastAPI
from routers import language
from fastapi.staticfiles import StaticFiles
app1 = FastAPI()

#Routers
app1.include_router(language.router)
app1.mount("/static",StaticFiles(directory="static"), name="static")


@app1.get("/")
async def root():
    return "Hola Mundo"
