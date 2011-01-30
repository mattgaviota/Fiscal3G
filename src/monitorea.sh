#!/bin/sh
awk -F "," '

    /espartanos/{
        gsub("\\\|", "")
        printf "%-30s %-12s", $1, $2
        system("sh src/resumen.sh " $2)
    }
' contacts.csv 2>/dev/null | sort > reporte.txt

awk '
    {
        printf "Votos: %4d  ", $(NF-4)
        printf "SMSs: %4d  ", $(NF-2)
        printf "Ultimo: %s  ", $NF
        printf "Numero: %10d\n", $(NF-6)
    }
' reporte.txt | sort -n > reporte_votos.txt
