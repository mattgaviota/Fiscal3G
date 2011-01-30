#!/bin/sh
uniq report_archive.csv | awk -v numero="$1," '$5~numero{print $0}'
uniq report_archive.csv | awk -v numero="$1," '
$5~numero{total++}
END{print "Envió", total, "votos"}
'

echo "Envió $(grep $1 inbox_archive.mbox|grep From:|wc -l) mensajes."

awk -v numero="$1" '

BEGIN{
    hora = "Nunca"
}

/From +/ && $2~numero{
    hora = $(NF - 1)
}

END{
    print "Envió el ultimo mensaje a las", hora
}

' inbox_archive.mbox
