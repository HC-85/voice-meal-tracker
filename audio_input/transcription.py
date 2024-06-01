import librosa

def transcribe(model, sr, audio_file, generate_kwargs):
    y, sr = librosa.load(audio_file, sr=sr)
    transcription = model(y, generate_kwargs=generate_kwargs)
    return transcription['text']