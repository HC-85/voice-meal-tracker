import pdb

def query_food_batch(model_sbert, food_index, foods, k = 3):
    idxs = []
    for food in foods:
        food_name = ', '.join(food['ingredients'])
        enc_food_name = model_sbert.encode(food_name)
        labels, _ = food_index.knn_query(enc_food_name, k = k)
        idxs.append(labels[0].astype(int).tolist())
    return idxs    