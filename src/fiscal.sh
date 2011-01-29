#!/bin/sh
while true; do
    python src/fiscal.py | tee -a general.log
    sleep 15
    timestamp sleep
done
