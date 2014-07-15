# -*- coding: utf-8 -*-
from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Lideria(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('@id', ''),
        'url':('@url', ''),
        'price':('@price', 0),
        'availability': ('@avail', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        'cover':("./imgs/main/@url", ''),
        'description':('./desc', ''),

        'authors':("./attrs/a[@name='Autor']", ''),
        'isbns':("./attrs/a[@name='ISBN']", ''),
        'page_count':("./attrs/a[@name='Ilosc_stron']", ''),
        'publisher':("./attrs/a[@name='Wydawnictwo']", ''),
        'date':("./attrs/a[@name='Rok_wydania']", ''),
        'cover_type':("./attrs/a[@name='Oprawa']", ''),
        'formats':("./attrs/a[@name='Format']", ''),
        #size
    }

    def adjust_parse(self, dic):
        if u"Księgarnia/Książki" in dic['category']:
            dic['size'] = dic['formats']
            dic['formats'] = ['ks']
        else:
            pass
            #TODO: T540 - add support for audiobooks and ebooks
            # + remember to edit fullfill condition in update.ini

class LideriaBook(GenericBook, Base):
    external_id = Column(Integer, unique = True)
    #url
    #pp_url
    #price
    availability = Column(Integer)
    category = Column(Unicode(64))
    #title
    #cover
    #description
    publisher = Column(Unicode(128))
    date = Column(Unicode(4))
    cover_type = Column(Unicode(64))
    #formats
    size = Column(Unicode(64))

