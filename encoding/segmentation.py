def segment_text(model_ner, text):
    entity_types = ['food', 'ingredient', 'brand', 'restaurant', 'measurement or quantity', 'numeral']
    entities = model_ner.predict_entities(text, entity_types, threshold=0.4)
    foods = []
    for entity in entities:
        match = entity['label']
        if match in ['measurement or quantity', 'numeral']:
            foods.append({})
            foods[-1]['quantity'] = entity["text"]

        elif match in ['food', 'ingredient']:
            other_ingredients = foods[-1].get('ingredients', [])
            foods[-1]['ingredients'] =  [*other_ingredients, entity["text"]]

        elif match in ['brand', 'restaurant']:
            foods[-1]['brand'] = entity["text"]
        
        else:
            assert(0)
    return foods
    