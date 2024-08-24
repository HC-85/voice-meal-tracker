import librosa
import re
from transformers import WhisperForConditionalGeneration as Whisper, pipeline
from typing import Union, Dict

def transcribe(model: Union[pipeline, Whisper], sr: int, audio_file: str, generate_kwargs: Dict[str, str]) -> str:
    y, sr = librosa.load(audio_file, sr=sr)
    transcription = model(y, generate_kwargs=generate_kwargs)
    transcription = re.sub(r'(?: 1)+$', '', transcription['text'].strip())
    return transcription