from fastapi import FastAPI
from app_transcribe import load_faster_whisper

app = FastAPI()

@app.on_event("startup")
def load_model():
    global model
    model = load_faster_whisper()


@app.post("/transcribe")
def transcribe_endpoint():
    pass