#!/bin/sh
if [ $# -lt 5 ] ;
    then echo "Usage: $0 <identify_file> <database> <host> <src_path> <dst_path>" ; exit  ; 
fi
export identity=$1
export db=$2
export host=$3
export src=$4
export dst=$5

mkdir -p $src 
mysqldump -u root ${db} > ${src}/${db}.db && gzip -f ${src}/${db}.db && rsync -av -e "ssh -i ${identity}" ${src} ${host}:${dst} && rm ${src}/${db}.db.gz

