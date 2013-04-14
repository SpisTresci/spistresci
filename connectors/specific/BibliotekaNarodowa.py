#!/usr/bin/env python

# ***** To run this, please Install PyZ3950: *****
# git clone git://github.com/asl2/PyZ3950.git PyZ3950
# cd PyZ3950
# sudo python setup.py install
#
# ********  PyZ3950 also need ply library: *******
# sudo easy_install ply

from PyZ3950 import zoom

BN_address = '193.59.172.100'

conn = zoom.Connection (BN_address, 210)
conn.databaseName = 'INNOPAC'
conn.preferredRecordSyntax = 'USMARC'

query = zoom.Query ('CCL', 'ti="Mickiewicz"')

res = conn.search (query)
for r in res:
    print r
conn.close ()