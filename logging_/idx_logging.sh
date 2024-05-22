#!/bin/bash

# arg1: food_idx
# arg2: timestamp
echo $1
echo $2
sqlite3 food_log.db "INSERT INTO food_idxs ('food_idx', 'timestamp') VALUES('$1', '$2');"
