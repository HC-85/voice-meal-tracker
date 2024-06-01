import torch
from setup.data_setup import load_food_dataset, load_food_index
from setup.model_setup import load_ner, load_sbert, load_whisper
from inference.ner_inference import entity_prediction, parse_entities
from inference.querying import query_food_batch
from logging_.simple_log import txt_log, sql_log
from logging_.retrieval import txt2df
from audio_input.fetching import fetch_voicenotes
from audio_input.transcription import transcribe
from os import listdir
from os.path import join as path_join

txt = """
150 grams of brown rice,
half a gram of dried basil,
150 grams of grilled chicked breast cooked with half a teaspoon of olive oil,
one Carl's Jr. double meat Portobello burger,
two fried chicken drumsticks from KFC
"""

audio_path = '/workspaces/Nutrition-Logger/audio_input/voicenotes/'
def main():
    index = load_food_index()
    dataset = load_food_dataset()
    whisper, sr = load_whisper()
    ner = load_ner()
    sbert = load_sbert()
    
    fetch_voicenotes(save_path = audio_path)

    for vn_file in listdir(audio_path):
        transcription = transcribe(whisper, sr, path_join(audio_path, vn_file), {"language": "english"})
        print('Transcript:\n')
        print(transcription, '\n')
        entities = entity_prediction(ner, transcription)
        foods = parse_entities(entities)
        idxs = query_food_batch(sbert, index, foods)
        
        sql_log(idxs, timestamp = vn_file[:16])


if __name__ == '__main__':
    main()