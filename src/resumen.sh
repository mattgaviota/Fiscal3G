#!/bin/sh

uniq report_archive.csv | awk -v numero="$1," '
    $5~numero{
        total++
    }

    END{
        printf "Votos: %-5d", total
    }
'

awk -v numero="$1" '
    /^From:/ && $2 ~ numero {
        total++
    }

    END{
        printf "  SMSs: %-5d", total
    }
' inbox_archive.mbox

awk -v numero="$1" '

    BEGIN{
        hora = "Nunca"
    }

    /From +/ && $2~numero{
        hora = $(NF - 1)
    }

    END{
        printf "  Ultimo: %-5s\n", hora
    }

' inbox_archive.mbox
