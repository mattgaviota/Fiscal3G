#!/bin/sh
echo $3|gnokii --config "$1" --sendsms "$2" -r
