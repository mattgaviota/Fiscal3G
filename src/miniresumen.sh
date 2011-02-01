#!/bin/sh

#VOTOS
VOTOS=$(
    uniq report_archive.csv | awk -v numero="$1" '
        $5~numero{
            total++
        }
        END{
            printf "%d", total
        }
    '
)

#SMSs
SMS=$(
    awk -v numero="$1" '
        /^From:/ && $2 ~ numero {
            total++
        }
        END{
            printf "%d", total
        }
    ' inbox_archive.mbox
)

#VOTOS/SMSs
VOTOSPORSMS=$(
    echo $VOTOS / $SMS|bc -l
)

#PRIMERO
PRIMERO=$(
    awk -v numero="$1" '
        BEGIN{
            hora = "999999"
        }
        $5~numero{
            sub(",", "", $(NF - 1))
            if (hora > $(NF -1))
                hora = $(NF - 1)
        }
        END{
            shora = substr(hora, 1, 2)
            sminu = substr(hora, 3, 2)
            ssegu = substr(hora, 5, 2)
            printf "%02d:%02d:%02d", shora, sminu, ssegu
        }
' report_archive.csv
)

#ULTIMO
ULTIMO=$(
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
            printf "%02d:%02d:%02d", shora, sminu, ssegu
        }
    ' report_archive.csv
)

#SEGSPORSMS
SEGSPORSMS=$(
    awk -v primero="$PRIMERO" -v ultimo="$ULTIMO" -v sms="$SMS" '
        BEGIN{
            split(primero, aprimero, ":")
            split(ultimo, aultimo, ":")
            time = aprimero[1] * 3600 + aprimero[2] * 60 + aprimero[3]
            print time / sms
        }
    '
)

#SEGSPORVOTO
SEGSPORVOTO=$(
    awk -v primero="$PRIMERO" -v ultimo="$ULTIMO" -v votos="$VOTOS" '
        BEGIN{
            split(primero, aprimero, ":")
            split(ultimo, aultimo, ":")
            time = aprimero[1] * 3600 + aprimero[2] * 60 + aprimero[3]
            print time / votos
        }
    '
)

echo "$VOTOS;$SMS;$VOTOSPORSMS;$PRIMERO;$ULTIMO;$SEGSPORSMS;$SEGSPORVOTO"
