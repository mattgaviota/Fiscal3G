#!/bin/sh
uniq report_archive.csv | awk -v numero="$1," '$5~numero{print $0}'

echo
sh src/resumen.sh $1
