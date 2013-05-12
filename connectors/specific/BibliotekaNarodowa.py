# -*- coding: utf-8 -*-
#!/usr/bin/env python

# ***** To run this, please Install PyZ3950: *****
# git clone git://github.com/asl2/PyZ3950.git PyZ3950
# cd PyZ3950
# sudo python setup.py install
#
# ********  PyZ3950 also need ply library: *******
# sudo easy_install ply

from datetime import datetime
from PyZ3950 import zoom, zmarc
from connectors.generic import *
import lxml.etree as et
import urllib2
import os
from sqlwrapper import *
import re
import glob

class BibliotekaNarodowa(XMLConnector, ReferenceConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./titleInfo[not(@type)]/title":('title', ''),
        #"./titleInfo[@type='alternative']/title":('title_alternative', ''),
        #"./titleInfo[not(@type)]/subtitle":('subtitle', ''),
        #"./titleInfo[@type='alternative']/subtitle":('subtitle_alternative', ''),
        u"./name[@type='personal' and not(./role/roleTerm[@type='text' and .='Tł.']) and contains(./role/roleTerm[@type='text'],'creator')]/namePart[not(@type)]":('authors', ''),
        u"./name[@type='personal' and ./role/roleTerm[@type='text' and .='creator'] and ./role/roleTerm[@type='text' and .='Tł.']]/namePart[not(@type)]":('translators', ''),
        "./genre[@authority='marcgt']":('genre', ''),
        "./originInfo/publisher":('publisher', ''),
        "./originInfo/dateIssued[@encoding='marc']":('date', ''),
        "./language/languageTerm":('lang', ''),
        "./physicalDescription/form[@authority='marcform']":('form', ''),
        "./identifier[@type='isbn']":('isbns', ''),
        #"./identifier[@type='isbn']":('external_id', ''),
    }

    def fetchData(self):
        self.conn = self.make_conn ()
        self.fetch_mods (zoom.Query ('CCL', 'isbn="978*"'))


    def make_conn(self):
        conn = zoom.Connection ('193.59.172.100', 210)
        conn.databaseName = 'INNOPAC'
        conn.preferredRecordSyntax = 'USMARC'
        return conn

    def fetch_mods(self, query):
        res_list = list(self.conn.search (query))
        dir_name = "data/" + datetime.now().strftime('%Y%m%d%H%M%S')
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        n = i = 0
        while i != len(res_list):
            filename = os.path.join(dir_name, "bibliotekanarodowa_%d.xml" % n)
            print "bibliotekanarodowa_%d.xml" % n
            f = open(filename, 'w')
            f.write("<root>")
            for j in range(5000):
                i = i + 1
                if i == len(res_list):
                    break
                marc_obj = zmarc.MARC (res_list[i].data, strict=0)
                f.write(marc_obj.toMODS ())
            f.write("</root>")
            n = n + 1

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validateLists(dic)
        self.validateISBNs(dic, id, title)
        self.validateAuthors(dic, id, title)
        self.validateAuthors(dic, id, title, "translators")


    def validateLists(self, dic):
        for tag_name in dic.keys():
            if dic.get(tag_name) != None:
                if isinstance (dic[tag_name], list) and len(dic[tag_name]) > 1:
                    if isinstance(dic[tag_name][0], dict) or dic[tag_name][0] == None:
                        dic[tag_name] = dic[tag_name][0]
                    else:
                        dic[tag_name] = unicode(dic[tag_name][0])


    #TODO
    def is_name(self, name):
        return True

    def validateAuthors(self, dic, id, title, tag_name='authors'):
        if dic.get(tag_name) != None:
            persons = dic[tag_name]
            new_list_of_person_dicts=[]
            pdict={}
            if not (isinstance(persons, list) and not isinstance(persons, str)):
                persons = [persons]
            for person in persons:
                pdict["name"] = person 
                names = [x.strip() for x in person.split(",")]
                if len(names) == 2: #imie i nazwisko
                    pdict["lastName"] = names[0].strip()
                    firstNames = names[1]
                    if " " in firstNames:
                        first_and_middle = firstNames.split(" ")
                        pdict["firstName"] = self.remove_dot_from_name(first_and_middle[0])
                        pdict["middleName"] = self.remove_dot_from_name(first_and_middle[1]) 
                    else:
                        pdict["firstName"] = self.remove_dot_from_name(firstNames)
                elif len(names) == 1:
                    print "1 - "  + person
                else:
                    print str(len(names)) + " - "  + person

                new_list_of_person_dicts.append(pdict)

            dic[tag_name] = new_list_of_person_dicts


    def remove_dot_from_name(self, name):
        return name[:-1] if (name.endswith(".") and self.is_name(name[:-1])) else name


Base = SqlWrapper.getBaseClass()

class BibliotekaNarodowaBook(GenericBook, Base):
    id =  Column(Integer, primary_key=True)
    title = Column(Unicode(512))                    #502
    genre = Column(Unicode(16))                     #4
    publisher = Column(Unicode(1024))               #118
    date = Column(Unicode(4))#, primary_key=True)
    lang = Column(Unicode(4))                       #
    form = Column(Unicode(8))                       #
