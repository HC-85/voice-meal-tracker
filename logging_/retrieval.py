import ast
import pandas as pd
import sqlite3
from prettytable import PrettyTable
import pdb


def txt2df(txt_file):
    with open(txt_file, 'r') as logfile:
        lines = logfile.readlines()

        food_log = []
        for line in lines:
            food_log.append(dict(ast.literal_eval(line[:-2])))
    
    food_df = pd.DataFrame(food_log)
    return food_df


def display_log():
    query=  """
            SELECT 
                n.product_name, 
                n.energy_100g,
                f.timestamp
            FROM 
                food_idxs AS f
            LEFT OUTER JOIN 
                nutrition_table AS n
            ON 
                f.food_idx = n.id;
            """
    with sqlite3.connect('/mnt/local/food_log.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        table = PrettyTable(['product_name', 'energy_100g', 'timestamp'])

        for row in results:
            table.add_row(row)
        print(table)

