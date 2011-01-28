#!/bin/sh
# Recive:
#    phonenumber as $1
#    date        as $2
#    content     as stdin

time=$(date +"%Y-%m-%d %T") #Human legible timestamp
file="$2.$time.$1"
echo $time $(tee "$file")
