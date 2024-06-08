from setup.data_setup import load_food_index, create_nutrition_table, load_food_dataset
from setup.model_setup import load_ner, load_sbert, load_whisper

from audio.fetching import fetch_voicenotes
from audio.transcription import transcribe

from encoding.segmentation import segment_text
from encoding.querying import query_food_batch

from logs.db_logging import sql_log
from logs.retrieval import display_log

from os import listdir, getcwd

import pdb
audio_path = path_join(getcwd(), 'audio/voicenotes')
def main() -> None:
    index = load_food_index()
    dataset = load_food_dataset()
    create_nutrition_table(dataset)
    
    ner = load_ner()
    sbert = load_sbert()
    fetch_voicenotes(save_path = audio_path)

    for vn_file in listdir(audio_path):
        transcription = transcribe(whisper, sr, path_join(audio_path, vn_file), {"language": "english"})

        foods = segment_text(ner, transcription)
        print('Foods:')
        print(foods)
        
        
        for food, idx in zip(foods, idxs):
            predictions = []
            for food_id in idx:
                predictions.append(dataset.select([food_id])['product_name'][0])
            print(f"{food['ingredients']} -> {predictions}")
        
        sql_log(idxs, timestamp = vn_file[:16])

    display_log()

if __name__ == '__main__':
    main()