#!/usr/bin/python
import sys, os, inspect

#found here 
#http://stackoverflow.com/questions/279237/import-a-module-from-a-folder/6098238#6098238
# use this if you want to include modules from a subforder
cmd_upfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],'..')))
if cmd_upfolder not in sys.path:
    sys.path.insert(0, cmd_upfolder)

from connectors import Tools
from connectors.generic import *
from sqlwrapper import *
import csv

def main():
    GenericConnector.config_file = 'conf/update.ini'
    GenericConnector.read_config()

    connector_classnames = Tools.get_classnames(GenericConnector.config_object)
    connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)(name=connector[0]) 
                                            for connector in connector_classnames .items() ]
    dic = {}

    connectors = sorted(connectors, cmp=lambda x,y: -1 if x.name.lower() < y.name.lower() else (1 if x.name.lower() > y.name.lower() else 0))

    for c in connectors:
        try:
            for key in c.xml_tag_dict.keys():
                val = c.xml_tag_dict[key][0]
                dic.setdefault(key, {'tag_name':key})
                dic[key][c.name] = unicode(val).encode('utf-8')
        
        except Exception as e :
            print >> sys.stderr, 'Error executing script for connector %s: %s' % (c, e)

    csv.register_dialect('our', delimiter = '~')
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None
    if filename:
        f = open(filename, 'wu')
    else:
        f = sys.stdout
    
    fieldnames = ['tag_name'] + [c.name for c in connectors]
    writer = csv.DictWriter(f, fieldnames = fieldnames, restval = '', extrasaction = 'ignore', dialect='our')
    writer.writerow(dict ((x,x) for x in  writer.fieldnames))
    for x in dic.keys():
        writer.writerow(dic[x])
    if filename:
        f.close()

if __name__ == '__main__':
    main()
