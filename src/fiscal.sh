#!/bin/sh
while true; do
    python src/fiscal.py | tee -a general.log
    timeout 300 python src/query.py to_db/* && rm to_db/* 2> /dev/null 
    sleep 5
    timestamp sleep
done
