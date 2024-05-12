from datasets import load_dataset
from huggingface_hub import hf_hub_download
import pickle

def load_food_index():
    food_index_path = hf_hub_download(repo_id="HC-85/open-food-facts", filename="food-index.pkl",  repo_type="dataset")
    with open(food_index_path, 'rb') as f:
        food_index = pickle.load(f)
    return food_index

def load_food_dataset():
    dataset = load_dataset('HC-85/open-food-facts', 'reduced')['train']
    dataset = dataset.filter(lambda x: [y == 'en' for y in x['lang']], batched = True)
    return dataset
