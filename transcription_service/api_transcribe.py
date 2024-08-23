from fastapi import FastAPI
from pydantic import BaseModel
from app_transcribe import load_faster_whisper, transcribe_all, transcribe_audio

app = FastAPI()

class Audio(BaseModel):
    file_path: str


@app.on_event("startup")
def load_model():
    global model
    model = load_faster_whisper(model_size='distil-small.en')


@app.post("/transcribe_audio")
def transcribe_endpoint(audio: Audio):
    transcription = transcribe_audio(model, audio.file_path)
    return {"transcription": transcription}


@app.post("/transcribe_all")
def transcribe_all_endpoint():
    transcription = transcribe_all(model)
    return {"transcription": transcription}


@app.get("/health")
def healthcheck():
    return "OK"