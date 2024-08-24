from sentence_transformers import SentenceTransformer as SBERT
from hnswlib import Index
from typing import List, Dict

def query_food(model_sbert:SBERT, food_index:Index, food:Dict, k:int = 3) -> List[int]:
    food_name = ', '.join(food['ingredients'])
    enc_food_name = model_sbert.encode(food_name)
    labels, _ = food_index.knn_query(enc_food_name, k = k)
    return labels[0].astype(int).tolist()


def query_food_batch(model_sbert:SBERT, food_index:Index, foods:dict, k:int = 3) -> List[List[int]]:
    idxs = []
    for food in foods:
        idxs.append(query_food(model_sbert, food_index, food, k))
    return idxs    