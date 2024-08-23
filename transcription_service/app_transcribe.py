from typing import Union, Dict

MODEL_ID = "openai/whisper-tiny"
MODEL_SAMPLE_RATE = 16_000

from faster_whisper import WhisperModel

def load_faster_whisper(model_size = "large-v3"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model


def transcribe(model, audio_file):
    
    segments, info = model.transcribe(audio_file, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    return list(segments)