#!/bin/sh
while true; do
    python src/fiscal.py | tee -a general.log
    timeout 30 python src/query.py to_db/* | tee -a report.log
    rm to_db/* 
    sleep 5
    timestamp sleep
done
