#!/bin/bash

sqlite3 food_log.db
sqlite3 "CREATE TABLE food_idxs (
           food_idx INTEGER NOT NULL,
           timestamp TEXT NOT NULL);"