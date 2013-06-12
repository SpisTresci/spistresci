#!/bin/sh
if [ $# -lt 2 ] ;
    then echo "Usage: $0 <htpasswd_file> [<list_of_bookstores>]" ; exit  ; 
fi
export filename=$1
shift
if [ ! -f $filename ] ; 
    then touch $filename ; 
fi
for ks in $@ ; 
    do export pass=`makepasswd --chars=8`$ks ; 
    echo $ks: $pass ; 
    htpasswd -b $filename $ks $pass 2> /dev/null ;
done
