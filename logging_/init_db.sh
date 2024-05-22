#!/bin/bash

sqlite3 food_log.db "CREATE TABLE IF NOT EXISTS food_idxs (food_idx INTEGER, timestamp TEXT);"