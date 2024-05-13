import ast
import pandas as pd


def txt2df(txt_file):
    with open(txt_file, 'r') as logfile:
        lines = logfile.readlines()

        food_log = []
        for line in lines:
            food_log.append(dict(ast.literal_eval(line[:-2])))
    
    food_df = pd.DataFrame(food_log)
    return food_df

