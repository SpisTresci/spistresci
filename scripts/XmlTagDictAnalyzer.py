#!/usr/bin/python
from connectors import Tools
from connectors.generic import *
from sqlwrapper import *

def main():
    GenericConnector.config_file = "xml_tag_conf/update.ini"
    GenericConnector.read_config()

    connector_classnames = Tools.get_classnames(GenericConnector.config_object)
    connectors = [ Tools.load_connector(connectorname=connector[1], config=GenericConnector.config_object)(name=connector[0]) 
                                            for connector in connector_classnames .items() ]
    sep = '~'
    con_name = "ConnectorName"
    dic = {con_name:" "}

    connectors = sorted(connectors, cmp=lambda x,y: -1 if x.name.lower() < y.name.lower() else (1 if x.name.lower() > y.name.lower() else 0))

    for c in connectors:

        list_of_keys = dic.keys()

        for key in c.xml_tag_dict.keys():
            nkey = c.xml_tag_dict[key][0]
            if dic.get(nkey) == None:
                dic[nkey] = ""
                for i in range(dic[con_name].count(sep)):
                    dic[nkey] += sep

            dic[nkey] += key + sep
            if nkey in list_of_keys:
                list_of_keys.remove(nkey)

        dic[con_name] += c.name + sep
        list_of_keys.remove(con_name)

        for key in list_of_keys:
            dic[key] += sep

    f = open("xml_tag_dict_analyze.csv", "w")

    f.write(con_name + sep + dic[con_name]+"\n")
    del dic[con_name]
    keys = sorted(dic.keys())
    for key in keys:
        f.write(key + sep + dic[key]+"\n")

    f.close()

if __name__ == '__main__':
    main()
