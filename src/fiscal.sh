#!/bin/sh
while true; do
    python src/fiscal.py | tee -a general.log
    sleep 5
    timestamp sleep
done
