#!/bin/sh
awk -F "," -v OFS=";" '

    /espartanos/{
        gsub("\\\|", "")
        system("sh src/miniresumen.sh " $2)
        print ";"$2, $1
    }
' contacts.csv 2>/dev/null | sort -n > reportebase.txt
