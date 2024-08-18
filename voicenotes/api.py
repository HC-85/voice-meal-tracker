from fastapi import FastAPI
from fetching import async_fetch

app = FastAPI()

@app.post("/fetch")
async def fetch_voicenotes():
    log = async_fetch()
    return log