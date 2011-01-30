#!/bin/sh
awk -v config="$1" -v smsfile="$2" '

NR==1{
    numero = $0
    }

NR==2{
    mensaje = $0
    }

END{
    system("echo \"" mensaje "\" |gnokii --config \"" config "\" --sendsms \""\
        numero "\" -r")
    }
    
' $2
