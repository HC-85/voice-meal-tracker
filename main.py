import torch
from setup.data_setup import load_food_dataset, load_food_index
from setup.model_setup import load_ner, load_sbert
from inference.ner_inference import entity_prediction, parse_entities
from inference.querying import query_food_batch
from logging_.simple_log import txt_log


txt = """
150 grams of brown rice,
half a gram of dried basil,
150 grams of grilled chicked breast cooked with half a teaspoon of olive oil,
one Carl's Jr. double meat Portobello burger,
two fried chicken drumsticks from KFC
"""


def main():
    index = load_food_index()
    dataset = load_food_dataset()
    ner = load_ner()
    sbert = load_sbert()
    
    #audio-retrieval
    #audio->txt
    entities = entity_prediction(ner, txt)
    foods = parse_entities(entities)
    idxs = query_food_batch(sbert, index, foods)
    txt_log(idxs)


if __name__ == '__main__':
    main()