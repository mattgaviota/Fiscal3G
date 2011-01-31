#!/bin/sh
awk -F "," -v OFS=";" '

    /espartanos/{
        gsub("\\\|", "")
        system("sh src/miniresumen.sh " $2)
        print ";"$2, $1
    }
' contacts.csv 2>/dev/null | sort -n > reportebase.txt

awk -F ";" -v OFS=";" '
    BEGIN{
        fmstr = "%-5s\t%-4s\t%8s\t%10s\t%s\n"
        printf fmstr, "VOTOS", "SMSs", "ULTIMO", "CELULAR", "APELLIDO NOMBRE"        
    }
    {
        printf fmstr, $1, $2, $3, $4, $5
    }
' reportebase.txt > reporte_votos.txt

awk -F ";" -v OFS=";" '
    BEGIN{
        fmstr = "%-4s\t%-5s\t%8s\t%10s\t%s\n"
        printf fmstr, "SMSs", "VOTOS", "ULTIMO", "CELULAR", "APELLIDO NOMBRE"        
    }
    {
        printf fmstr, $2, $1, $3, $4, $5
    }
' reportebase.txt > reporte_smss.txt

