from datetime import datetime, timezone, timedelta
from os.path import exists

tz = timezone(timedelta(hours=-6))

def txt_log(idxs):
    curr_time = datetime.now(tz).isoformat()

    new_flag = False
    if not exists('log.txt'):
        new_flag = True
        with open('log.txt', 'a') as logfile:
            logfile.write('[')
        

    with open('log.txt', 'r+') as logfile:
        # [[...],
        #   ...
        #  [...],
        #]
        logfile.seek(0, 2)
        if not new_flag:
            end_position = logfile.tell() 
            logfile.seek(max(0, end_position - 2))
            logfile.write(",\n")

        for idx in idxs:
            log_entry = [["timestamp", curr_time], ["food_idx", idx]]
            logfile.write(f'{log_entry},\n') 
        
        end_position = logfile.tell()
        logfile.seek(max(0, end_position-2))
        logfile.write(']') 
        
