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

class BibliotekaNarodowa(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./titleInfo[not(@type)]/title":('title', ''),
        "./titleInfo[@type='alternative']/title":('title_alternative', ''),
        "./titleInfo[not(@type)]/subtitle":('subtitle', ''),
        "./titleInfo[@type='alternative']/subtitle":('subtitle_alternative', ''),
        u"./name[@type='personal' and not(./role/roleTerm[@type='text' and .='Tł.']) and contains(./role/roleTerm[@type='text'],'creator')]/namePart[not(@type)]":('authors', ''),
        u"./name[@type='personal' and ./role/roleTerm[@type='text' and .='creator'] and ./role/roleTerm[@type='text' and .='Tł.']]/namePart[not(@type)]":('translators', ''),
        #"./genre[@authority='marcgt']":('genre', ''),
        #"./originInfo/publisher":('publisher', ''),
        #"./originInfo/dateIssued[@encoding='marc']":('date', ''),
        #"./language/languageTerm":('lang', ''),
        #"./physicalDescription/form[@authority='marcform']":('form', ''),
        #"./identifier[@type='isbn']":('isbn', ''),
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

    def parse(self):
        dirname = self.backup_dir if self.unpack_dir == '' else self.unpack_dir
        filename = self.filename if self.unpack_file == '' else self.unpack_file

        filename = os.path.join(dirname, filename)

        #files = glob.glob(self.backup_dir + '*.xml')
        #for filename in files:
        root = et.parse(filename).getroot()

        for book in root:
            dic = self.makeDict(book)
            print dic
            #self.validate(dic)
            #self.measureLenghtDict(dic)
            #self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key + ": " + unicode(self.max_len_entry[key])

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validateLists(dic)
        self.validateAuthors(dic, id, title)


    def validateLists(self, dic):
        for tag_name in dic.keys():
            if dic.get(tag_name) != null:
                if isinstance (dic[tag_name], list) and len(dic[tag_name]) > 1:
                    if isinstance(dic[tag_name][0], dict) or dic[tag_name][0] == None:
                        dic[tag_name] = dic[tag_name][0]
                    else:
                        dic[tag_name] = unicode(dic[tag_name][0])

    def validateAuthors(self, dic, id, title, tag_name='persons'):
        if dic.get(tag_name) != None:
            persons_list_of_dicts = dic[tag_name]
            if not isinstance(persons_list_of_dicts, list):
                persons_list_of_dicts = [persons_list_of_dicts]
            for person in persons_list_of_dicts:
                if person.get('personType') == 'creator' or (isinstance(person.get('personType'), list) and 'creator' in person.get('personType')):
                    if person.get('personName') != None and len(person['personName']) >= 1:
                        if dic.get('authors') == None:
                            dic['authors'] = []
                        dic['authors'].append(person['personName'][0].strip())
                if person.get('personType') == u'T\xc5.' or (isinstance(person.get('personType'), list) and u'T\xc5.' in person.get('personType')):
                    if person.get('personName') != None and len(person['personName']) >= 1:
                        if dic.get('translators') == None:
                            dic['translators'] = []
                        dic['translators'].append(person['personName'][0].strip())

        dic['authors']

    #GenericConnector.validateAuthors(dic, id, title, tag_name='authors')
        #GenericConnector.validateAuthors(dic, id, title, tag_name='translators')
    def splitAuthor(self, dic, tag_name):
        name = dic[tag_name].split(",")
        person = {}
        if len(name) == 2:
        #imie i nazwisko
            if not " " in name[1]:
                person['firstName'] = name[1]
            else:
                sec_name = name[1].split(" ")
        person['firstName'] = sec_name[0]
        person['secondName'] = sec_name[1]
        person['lastName'] = name[0]






Base = SqlWrapper.getBaseClass()

class BibliotekaNarodowaBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512))        #502
    subtitle = Column(Unicode(2048))    #109
    #authors
    genre = Column(Unicode(16))         #4
    isbn = Column(Unicode(13))          #
    publisher = Column(Unicode(1024))        #118
    date = Column(Integer)             #GROSZE!!!
    lang = Column(Unicode(4))          #
    form = Column(Unicode(8))          #
    external_id = Column(Unicode(16))      #


class BibliotekaNarodowaBookDescription(GenericBookDescription, Base):
    pass

class BibliotekaNarodowaAuthor(GenericAuthor, Base):
    pass

class BibliotekaNarodowaBookPrice(GenericBookPrice, Base):
    pass

class BibliotekaNarodowaBooksAuthors(GenericBooksAuthors, Base):
    pass
