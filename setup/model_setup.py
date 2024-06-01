from gliner import GLiNER
from sentence_transformers import SentenceTransformer
import torch
import transformers

device = 'cuda' if torch.cuda.is_available() else 'cpu'
transformers.__version__ = transformers.__version__[:-5] #'4.41.0.dev0' -> '4.41.0'

def load_ner():
    model_ner = GLiNER.from_pretrained("urchade/gliner_large-v2.1", device = device)
    return model_ner

def load_sbert():
    model_sbert = SentenceTransformer("all-MiniLM-L6-v2", device = device)
    return model_sbert

def load_whisper():
    from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
    whisper_ver = "openai/whisper-large-v3"
    model_whisper = WhisperForConditionalGeneration.from_pretrained(whisper_ver)

    if device == "cuda":
        torch_dtype = torch.float16
        model_whisper = model_whisper.half()
    else:
        torch_dtype = torch.float32

    processor_whisper = WhisperProcessor.from_pretrained(whisper_ver, device = device)

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