#!/bin/bash

# arg1: food_idx
# arg2: timestamp

sqlite3 "food_log.db INSERT INTO food_idx VALUES($1, $2);"
