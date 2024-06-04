from gliner import GLiNER
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
#import transformers
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
#transformers.__version__ = transformers.__version__[:-5] #'4.41.0.dev0' -> '4.41.0'

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_ner():
    print("Loading GLiNER...")
    model_id = "urchade/gliner_large-v2.1"
    model_ner = GLiNER.from_pretrained(model_id, device = device)
    return model_ner

def load_sbert():
    print("Loading SBERT...")
    model_id = "all-MiniLM-L6-v2"
    model_sbert = SentenceTransformer(model_id, device = device)
    return model_sbert

def load_whisper():
    print("Loading Whisper...")
    model_id = "openai/whisper-tiny"
    model_whisper = WhisperForConditionalGeneration.from_pretrained(model_id)

    if device == "cuda":
        torch_dtype = torch.float16
        model_whisper = model_whisper.half()
    else:
        torch_dtype = torch.float32

    processor_whisper = WhisperProcessor.from_pretrained(model_id, device = device)
    processor_whisper.tokenizer.pad_token = processor_whisper.tokenizer.eos_token
    
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


def load_distil_whisper():
    print("Loading Distil-Whisper...")
    model_id = "distil-whisper/distil-large-v3"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, 
                                                      low_cpu_mem_usage=True, use_safetensors=True)
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=25,
        batch_size=16,
        max_new_tokens=128,
        return_timestamps=False,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe, 16_000