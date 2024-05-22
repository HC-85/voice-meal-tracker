from datetime import datetime, timezone, timedelta
from os.path import exists
from subprocess import run

tz = timezone(timedelta(hours=-6))

def txt_log(idxs):
    curr_time = datetime.now(tz).isoformat()

    with open('./log.txt', 'a') as logfile:
        for idx in idxs:
            log_entry = [["timestamp", curr_time], ["food_idx", idx]]
            logfile.write(f'{log_entry},\n')  

def sql_log(idxs):

    if not exists('./food_log.db'):
        try:
            result = run(['./init_db.sh'], check=True, capture_output=True, text=True)  
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")

    curr_time = datetime.now(tz).isoformat()

    for idx in idxs:
        try:
            result = subprocess.run(['./idx_logging.sh', idx, curr_time], check=True, capture_output=True, text=True)
            print("Output:", result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            print(f"Return Code: {e.returncode}") 