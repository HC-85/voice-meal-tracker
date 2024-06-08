from setup.data_setup import load_food_dataset, load_food_index, create_nutrition_table
from setup.model_setup import load_ner, load_sbert, load_distil_whisper, load_whisper
from inference.ner_inference import entity_prediction, parse_entities
from inference.querying import query_food_batch
from logging_.simple_log import sql_log
from logging_.retrieval import display_log
from audio_input.fetching import fetch_voicenotes
from audio_input.transcription import transcribe
from os import listdir
from os.path import join as path_join
from os.path import exists


audio_path = '/workspaces/Nutrition-Logger/audio_input/voicenotes/'
def main():
    index = load_food_index()
    dataset = load_food_dataset()
    if not exists("/mnt/local/food_log.db"):
        create_nutrition_table(dataset)
    
    whisper, sr = load_whisper()
    ner = load_ner()
    sbert = load_sbert()

    fetch_voicenotes(save_path = audio_path)

    for vn_file in listdir(audio_path):
        transcription = transcribe(whisper, sr, path_join(audio_path, vn_file), {"language": "english"})
        print('Transcript:')
        print(transcription, '\n')
        entities = entity_prediction(ner, transcription)
        print('Entities:')
        print(entities)
        foods = parse_entities(entities)
        print('Foods:')
        print(foods)
        idxs = query_food_batch(sbert, index, foods, k=3)

        for food, idx in zip(foods, idxs):
            predictions = []
            for food_id in idx:
                predictions.append(dataset.select([food_id])['product_name'][0])
            print(f"{food['ingredients']} -> {predictions}")
        
        sql_log(idxs, timestamp = vn_file[:16])

    display_log()

if __name__ == '__main__':
    main()