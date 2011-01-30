#!/bin/sh
awk -F "," '

    /espartanos/{
        gsub("\\\|", "")
        system("sh src/resumen.sh " $2)
        printf "  %-30s %-12s\n", $2, $1
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

awk '
    {
        printf "SMSs: %4d  ", $(NF-2)
        printf "Votos: %4d  ", $(NF-4)
        printf "Ultimo: %s  ", $NF
        printf "Numero: %10d\n", $(NF-6)
    }
' reporte.txt | sort -n > reporte_smss.txt

awk '
    {
        printf "Ultimo: %s  ", $NF
        printf "Votos: %4d  ", $(NF-4)
        printf "SMSs: %4d  ", $(NF-2)
        printf "Numero: %10d\n", $(NF-6)
    }
' reporte.txt | sort -n > reporte_ultimo.txt
