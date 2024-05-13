from datetime import datetime, timezone, timedelta
from os.path import exists

tz = timezone(timedelta(hours=-6))

def txt_log(idxs):
    curr_time = datetime.now(tz).isoformat()

    with open('logging_/log.txt', 'a') as logfile:
        for idx in idxs:
            log_entry = [["timestamp", curr_time], ["food_idx", idx]]
            logfile.write(f'{log_entry},\n')  
