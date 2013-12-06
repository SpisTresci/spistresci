from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()
class Ksiazki(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id', ''),
        'price': ('@price', 0),
        'url': ('@url', ''),
        'availability': ('@avail', ''),
        'category': ('./cat', ''),
        'title': ('./name', ''),
        'raw_title': ('./name', ''),
        'cover': ('./imgs/main/@url', ''),
        'description': ('./desc', ''),
        'isbns': ("./attrs/a[@name='ISBN']", ''),
        'publisher': ("./attrs/a[@name='Wydawnictwo']", ''),
        'formats': ("./attrs/a[@name='Format']", ''),
        'authors':("./attrs/a[@name='Autor']", ''),
        'publisher':("./attrs/a[@name='Wydawnictwo']", ''),
        'page_count': ("./attrs/a[@name='Ilosc_stron']", ''),
        'date': ("./attrs/a[@name='Rok_wydania']", ''),
        'sample': ("./attrs/a[@name='Fragment']", ''),


    }

    def adjust_parse(self, dic):
        title = dic['title']
        if ' (e-book)' in title:
            title = title.replace(' (e-book)','')
            dic['title'] = title

#{'raw_title': 150, 'description': 17690, 'price': 5, 'page_count': 4, 'sample': 39, 'authors': 228, 'date': 4, 'availability': 1, 'category': 70, 'publisher': 25, 'title': 150, 'url': 182, 'cover': 74, 'isbns': 17, 'formats': 13, 'external_id': 11}

class KsiazkiBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    category = Column(Unicode(128))      #70
    title = Column(Unicode(256))        #150
    raw_title = Column(Unicode(256))        #150
    url = Column(Unicode(256))           #182
    cover = Column(Unicode(128))        #74
    price = Column(Integer)
    availability = Column(Boolean)
    publisher = Column(Unicode(64))     #25
    page_count = Column(Integer)
    date = Column(Date)                 #
    sample = Column(Unicode(64))        #39
