def query_food(model_sbert, food_index, food, k = 3):
    food_name = ', '.join(food['ingredients'])
    enc_food_name = model_sbert.encode(food_name)
    labels, _ = food_index.knn_query(enc_food_name, k = k)
    return labels[0].astype(int).tolist()


def query_food_batch(model_sbert, food_index, foods, k = 3):
    idxs = []
    for food in foods:
        idxs.append(query_food(model_sbert, food_index, food, k))
    return idxs    