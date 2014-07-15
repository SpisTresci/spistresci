#!/bin/sh
if [ $# -lt 5 ] ;
    then echo "Usage: $0 <identify_file> <database> <host> <src_path> <dst_path>" ; exit  ; 
fi
export identity=$1
export db=$2
export host=$3
export src=$4
export dst=$5
export date=`date +%Y%m%d_%H%M`
mkdir -p $src 
mysqldump -u root ${db} > ${src}/${db}_${date}.db && gzip -f ${src}/${db}_${date}.db && rsync -av -e "ssh -i ${identity}" ${src} ${host}:${dst} && rm ${src}/${db}_${date}.db.gz

