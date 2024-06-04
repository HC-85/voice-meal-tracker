from gliner import GLiNER
from sentence_transformers import SentenceTransformer
import torch
#import transformers
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
#transformers.__version__ = transformers.__version__[:-5] #'4.41.0.dev0' -> '4.41.0'

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_ner():
    print("Loading GLiNER...")
    model_ver = "urchade/gliner_large-v2.1"
    model_ner = GLiNER.from_pretrained(model_ver, device = device)
    return model_ner

def load_sbert():
    print("Loading SBERT...")
    model_ver = "all-MiniLM-L6-v2"
    model_sbert = SentenceTransformer(model_ver, device = device)
    return model_sbert

def load_whisper():
    print("Loading Whisper...")
    model_ver = "openai/whisper-large-v3"
    model_whisper = WhisperForConditionalGeneration.from_pretrained(model_ver)

    if device == "cuda":
        torch_dtype = torch.float16
        model_whisper = model_whisper.half()
    else:
        torch_dtype = torch.float32

    processor_whisper = WhisperProcessor.from_pretrained(model_ver, device = device)

    pipe_whisper = pipeline(
        "automatic-speech-recognition",
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
    return pipe_whisper, 16_000