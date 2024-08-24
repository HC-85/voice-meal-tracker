from datasets import load_dataset, Dataset
from huggingface_hub import hf_hub_download
import pickle
import sqlite3
from tqdm import tqdm
from os.path import exists
from hnswlib import Index
from typing import Union


def load_food_index() -> Index:
    food_index_path = hf_hub_download(repo_id="HC-85/open-food-facts", filename="food-index.pkl",  repo_type="dataset")
    with open(food_index_path, 'rb') as f:
        food_index = pickle.load(f)

    return food_index

def load_food_dataset() -> Dataset:
    dataset = load_dataset('HC-85/open-food-facts', 'reduced')['train']
    dataset = dataset.filter(lambda x: [y == 'en' for y in x['lang']], batched = True)
    return dataset

def create_nutrition_table(dataset:Dataset) -> None:
    if not exists("/mnt/local/food_log.db"):
        schema = """CREATE TABLE IF NOT EXISTS nutrition_table (
            id INTEGER PRIMARY KEY,
            product_name TEXT, 
            energy_100g TEXT
            )"""

        with sqlite3.connect('/mnt/local/food_log.db', isolation_level = 'DEFERRED') as conn:
            cursor = conn.cursor()
            cursor.execute(schema)

            print("Creating nutrition_table...")
            for item in tqdm(dataset):
                cursor.execute('INSERT INTO nutrition_table (product_name, energy_100g) VALUES (?, ?)', 
                (item['product_name'], item['energy_100g']))

            conn.commit()
        return dataset
        
    else:
        print("Food log already exists.")
        return None
    