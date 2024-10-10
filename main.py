from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/front", StaticFiles(directory="front"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test_data")
async def test_data():
    return {"data": [
        ['Task', 'Hours per Day'],
        ['Work',     11],
        ['Eat',      2],
        ['Commute',  2],
        ['Play', 2],
        ['Sleep',    7]
    ]}