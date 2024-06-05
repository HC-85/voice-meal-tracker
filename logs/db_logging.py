from tqdm import tqdm
import sqlite3

def sql_log(idxs, timestamp):
    schema = """CREATE TABLE IF NOT EXISTS food_idxs (
        food_idx INTEGER, 
        timestamp TEXT,
        FOREIGN KEY (food_idx) REFERENCES nutrition_table(id)
        )"""

    with sqlite3.connect('/mnt/local/food_log.db', isolation_level = 'DEFERRED') as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        for idx in tqdm(idxs):
            cursor.execute('INSERT INTO food_idxs (food_idx, timestamp) VALUES (?, ?)', (idx[0] + 1 , timestamp))

        conn.commit()