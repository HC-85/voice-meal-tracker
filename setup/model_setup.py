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