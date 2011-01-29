#!/bin/sh
while True; do
    python src/fiscal.py | tee -a general.log
    echo "Pausando el servidor..."
    sleep 5
done
