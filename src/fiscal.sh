#!/bin/sh
for config in $(find configs -type f) ; do
    echo $config
done
