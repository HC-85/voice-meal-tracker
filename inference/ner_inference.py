def entity_prediction(model_ner, text):
    entity_types = ['food', 'ingredient', 'brand', 'restaurant', 'measurement or quantity', 'numeral']
    entities = model_ner.predict_entities(text, entity_types, threshold=0.4)
    return 
    
def parse_entities(entities):
    foods = []
    for entity in entities:
        match entity['label']:
            case 'measurement or quantity' | 'numeral':
                foods.append({})
                foods[-1]['quantity'] = entity["text"]

            case 'food' | 'ingredient':
                other_ingredients = foods[-1].get('ingredients', [])
                foods[-1]['ingredients'] =  [*other_ingredients, entity["text"]]

            case 'brand'|'restaurant':
                foods[-1]['brand'] = entity["text"]
    return foods