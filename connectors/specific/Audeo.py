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

    #Try getting authors from description
    def getAuthorsFromDescription(self, dic, name):
        #TODO: Not implemented yet
        pass

    def adjust_parse(self, dic):
        if dic['authors'] == ['Praca Zbiorowa'] or dic['authors'] == ['Zbiorowy']:
            self.getAuthorsFromDescription(dic, u"Autor", "authors")

class AudeoBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(256))          #152
    availability = Column(Integer)
    category = Column(Unicode(64))      #33
    title = Column(Unicode(256))        #136
    cover = Column(Unicode(128))        #118
    time = Column(Integer)
    producent = Column(Unicode(64))     #35

