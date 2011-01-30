#!/bin/sh
awk -F "," '

    /espartanos/{
        gsub("\\\|", "")
        printf "%-30s %-12s", $1, $2
        system("sh src/resumen.sh " $2)
    }

' contacts.csv 2>/dev/null |sort > reporte.txt
