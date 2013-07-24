from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Audeo(Ceneo):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('@id', ''),
        'price':('@price', 0),
        'url':('@url', ''),
        'availability': ('@avail', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        'cover':("./imgs/main[@url]", ''),
        'description':('./desc', ''),
        'producent':("./attrs/a[@name='Producent']", ''),
        'authors':("./attrs/a[@name='Autor']", ''),
        'lectors':("./attrs/a[@name='Lektor']", ''),
        'time':("./attrs/a[@name='Czas (min)']", ''),
    }

    def adjust_parse(self, dic):
        if dic.get('authors') == ['Zbiorowy']:
            dic['authors'] = ['Praca Zbiorowa']
        #Audeo has only books in mp3 format.
        #We have this hardcoded.
        dic['formats'] = ['mp3']

class AudeoBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id
    #title = Column(Unicode(256))
    #price = Column(Integer)
    #price_normal
    #url = Column(Unicode(256))          #152
    cover = Column(Unicode(128))        #118
    availability = Column(Integer)
    category = Column(Unicode(64))      #33
    time = Column(Integer)
    producent = Column(Unicode(64))     #35

