from faster_whisper import WhisperModel


def load_faster_whisper(model_size = "tiny.en"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model


def transcribe(model, audio_file):
    segments, _ = model.transcribe(audio_file, beam_size=5)
    return [segment.text for segment in segments]