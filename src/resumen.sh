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
        hora = "000000"
    }

    $5~numero{
        sub(",", "", $(NF - 1))
        if (hora < $(NF -1))
            hora = $(NF - 1)
    }

    END{
        shora = substr(hora, 1, 2)
        sminu = substr(hora, 3, 2)
        ssegu = substr(hora, 5, 2)
        printf "  Ultimo: %2d:%2d:%d\n", shora, sminu, ssegu
    }

' report_archive.csv
