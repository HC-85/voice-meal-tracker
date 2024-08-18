from fastapi import FastAPI
from fetching import fetch, clear_cache

app = FastAPI()

@app.post("/fetch")
async def fetch_endpoint():
    logs = await fetch()
    return {"logs": logs}


@app.delete("/clear-cache")
def clear_cache_endpoint():
    logs = clear_cache()
    return {"logs": logs}