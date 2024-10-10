from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/front", StaticFiles(directory="front"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}