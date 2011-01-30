#!/bin/sh
uniq report_archive.csv|grep "$1,"
echo "Envió $(grep $1, report_archive.csv|wc -l) votos."
echo "Envió $(grep $1 inbox_archive.mbox|grep From:|wc -l) mensajes."
awk '

/From +/{
    hora = $(NF - 1)
}

END{
    print "Envió el ultimo mensaje a las", hora
}' inbox_archive.mbox
