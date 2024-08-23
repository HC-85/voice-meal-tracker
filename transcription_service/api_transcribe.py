from fastapi import FastAPI
from pydantic import BaseModel
from app_transcribe import load_faster_whisper, transcribe

app = FastAPI()

class Audio(BaseModel):
    file_path: str

@app.on_event("startup")
def load_model():
    global model
    model = load_faster_whisper()


@app.post("/transcribe")
def transcribe_endpoint(audio: Audio):
    transcription = transcribe(model, audio.file_path)
    return transcription

@app.get("/health")
def healthcheck():
    return "OK"