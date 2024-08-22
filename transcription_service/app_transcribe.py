"""import librosa
import re
from transformers import WhisperForConditionalGeneration as Whisper, pipeline, WhisperProcessor
from typing import Union, Dict
import torch

MODEL_ID = "openai/whisper-tiny"
MODEL_SAMPLE_RATE = 16_000


def load_whisper(device:str='cpu') -> pipeline:
    model_whisper = Whisper.from_pretrained(MODEL_ID)
    
    match device:
        case "cuda":
            torch_dtype = torch.float16
            model_whisper = model_whisper.half()
        case "cpu":
            torch_dtype = torch.float32
        case _:
            raise ValueError(f"Invalid device: {device}")

    processor_whisper = WhisperProcessor.from_pretrained(MODEL_ID, device=device)
    processor_whisper.tokenizer.pad_token = processor_whisper.tokenizer.eos_token
    
    pipe_whisper = pipeline(
        task = "automatic-speech-recognition",
        model=model_whisper,
        tokenizer=processor_whisper.tokenizer,
        feature_extractor=processor_whisper.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=False,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe_whisper

def transcribe(model: Union[pipeline, Whisper], 
               audio_file: str, 
               generate_kwargs: Dict[str, str]) -> str:
    
    y,_ = librosa.load(audio_file, sr=MODEL_SAMPLE_RATE)
    transcription = model(y, generate_kwargs=generate_kwargs)
    transcription = re.sub(r'(?: 1)+$', '', transcription['text'].strip())
    return transcription"""


from faster_whisper import WhisperModel

audio_file = "/vn_cache/2024-06-06_01-09_MM4986b3565a31c8a79b02b9a3ac0cecec.ogg"
def load_faster_whisper(model_size = "large-v3"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))