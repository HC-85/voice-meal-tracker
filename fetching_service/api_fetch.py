from fastapi import FastAPI
from pydantic import BaseModel
from app_fetch import fetch, clear_cache

app = FastAPI()

class Credentials(BaseModel):
    username: str
    password: str


@app.post("/fetch")
async def fetch_endpoint(credentials: Credentials):
    logs = await fetch(credentials)
    return {"logs": logs}


@app.delete("/clear-cache")
def clear_cache_endpoint():
    logs = clear_cache()
    return {"logs": logs}


@app.get("/health")
def healthcheck():
    return "OK"