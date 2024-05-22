# Nutrition Logger v0.1
Goal: Effortlessly keep track of nutrition with your phone via voice.

## Usage
1. **Open repo in Codespaces**:\
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/HC-85/Nutrition-Logger)

## Status
1. **Audio retrieval** -  *pending*
   - TODO: Set up bot with Twilio
2. **Audio to text** -  *pending*
   - TODO: Find suitable voice-to-text model (Whisper?)
3. **Text segmentation**:
   - _Currently_: GLiNER (large-v2.1)
   - TODO: Fine-tune to food-related labels.
4. **Vector encoding**:
   - _Currently_: SBERT (all-MiniLM-L6-v2)
   - TODO: Fine tune with food-related topics sentences.
5. **Data Querying**:
   - _Currently_: HNSW index from encoding English subset of columns `brand`+`prod_name`+`gen_name` of the [Open Food Facts dataset](https://huggingface.co/datasets/HC-85/open-food-facts/viewer/reduced).
   (See preprocessing/preprocess.py)
   - TODO: explore using separate indexes and weighting.
6. **Logging**:
   - _Currently_: simply append lines to `log.txt` as `[timestamp, idx]`
7. **Log Inspection**:
   - _Currently_: Turn text file to DataFrame.
   - TODO: Deploy visualization with a Phoenix webpage or maybe a HuggingFace Space
8. **Reinforcement** - *pending*
   - TODO: Allow user to correct entries and use these corrections for reinforcement.
