from setup.data_setup import load_food_index, create_nutrition_table
from setup.model_setup import load_ner, load_sbert, load_whisper

from audio.fetching import fetch_voicenotes
from audio.transcription import transcribe

from encoding.segmentation import segment_text
from encoding.querying import query_food_batch

from logs.db_logging import sql_log
from logs.retrieval import display_log

from os import listdir
from os.path import join as path_join
from os.path import exists

import pdb

audio_path = 'audio/voicenotes'
def main():
    pdb.set_trace()
    index = load_food_index()
    _ = create_nutrition_table()
    
    whisper, sr = load_whisper()
    ner = load_ner()
    sbert = load_sbert()

    fetch_voicenotes(save_path = audio_path)

    for vn_file in listdir(audio_path):
        transcription = transcribe(whisper, sr, path_join(audio_path, vn_file), {"language": "english"})
        print('Transcript:')
        print(transcription, '\n')

        foods = segment_text(ner, transcription)
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