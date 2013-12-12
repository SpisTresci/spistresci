from connectors.generic import GenericBook
from connectors.common import Ceneo

from sqlwrapper import *
class KsiazkiFabrykaBase(Ceneo):

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
        if self.title_suffix in title:
            title = title.replace(self.title_suffix,'')
            dic['title'] = title

class KsiazkiFabrykaBaseBook(GenericBook):
    #id = Column(Integer, primary_key = True)
    category = Column(Unicode(128))
    #title = Column(Unicode(256))
    raw_title = Column(Unicode(256))
    #url = Column(Unicode(256))
    #cover = Column(Unicode(256))
    #price = Column(Integer)
    availability = Column(Boolean)
    publisher = Column(Unicode(64))
    page_count = Column(Integer)
    date = Column(Date)
    sample = Column(Unicode(64))
