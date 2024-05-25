#!/bin/bash

# arg1: food_idx
# arg2: timestamp
sqlite3 food_log.db "INSERT INTO food_idxs ('food_idx', 'timestamp') VALUES('$1', '$2');"