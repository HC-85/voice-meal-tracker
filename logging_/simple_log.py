from datetime import datetime, timezone, timedelta
from os.path import exists
from subprocess import run, CalledProcessError
from tqdm import tqdm
import sqlite3


tz = timezone(timedelta(hours=-6))
base_path = 'logging_/'

def txt_log(idxs):
    curr_time = datetime.now(tz).isoformat()

    with open(base_path + 'log.txt', 'a') as logfile:
        for idx in idxs:
            log_entry = [["timestamp", curr_time], ["food_idx", idx]]
            logfile.write(f'{log_entry},\n')  


def sql_bash_log(idxs):
    print("Creating food_log.db ...")
    try:
        result = run([base_path + 'init_db.sh'], check=True, capture_output=True, text=True)  
        print("food_log.db ready.")
    except CalledProcessError as e:
        print(f"Error: {e.stderr}")
        
    curr_time = datetime.now(tz).isoformat()

    for idx in tqdm(idxs):
        try:
            result = run([base_path + 'idx_logging.sh', str(idx), str(curr_time)], check=True, capture_output=True, text=True)
            print("Output:", result.stdout)

        except CalledProcessError as e:
            print(f"Error: {e.stderr}")
            print(f"Return Code: {e.returncode}") 


def sql_log(idxs, timestamp):
    schema = """CREATE TABLE IF NOT EXISTS food_idxs (
        food_idx INTEGER, 
        timestamp TEXT,
        FOREIGN KEY (food_idx) REFERENCES nutrition_table(id)
        )"""

    with sqlite3.connect('/mnt/local/food_log.db', isolation_level = 'DEFERRED') as conn:
        cursor = conn.cursor()
        cursor.execute(schema)
        for idx in idxs:
            cursor.execute('INSERT INTO food_idxs (food_idx, timestamp) VALUES (?, ?)', (idx[0] + 1 , timestamp))

        conn.commit()