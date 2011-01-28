#!/bin/sh
# Recive:
#    phonenumber as $1
#    date        as $2
#    content     as stdin

time=$(date +"%Y-%m-%d_%T") #Human legible timestamp

cat > $time.$date.$phonenumber
