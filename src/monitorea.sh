#!/bin/sh
awk -F "," '

    /espartanos/{
        gsub("\\\|", "")
        system("sh src/miniresumen.sh " $2)
        printf "  %-12d %-30s\n", $2, $1
    }
' contacts.csv 2>/dev/null | sort -n > reporte.txt

awk '
    {
        printf "Votos: %4d  ", $1
        printf "SMSs: %4d  ", $2
        printf "Ultimo: %s  ", $3
        printf "    %s\n", substr($0, 20, 100)
    }
' reporte.txt | sort -n > reporte_votos.txt

awk '
    {
        printf "SMSs: %4d  ", $2
        printf "Votos: %4d  ", $1
        printf "Ultimo: %s  ", $3
        printf "    %s\n", substr($0, 20, 100)
    }
' reporte.txt | sort -n > reporte_smss.txt

awk '
    {
        printf "Ultimo: %s  ", $3
        printf "Votos: %4d  ", $1
        printf "SMSs: %4d  ", $2
        printf "    %s\n", substr($0, 20, 100)
    }
' reporte.txt | sort -n > reporte_ultimo.txt
