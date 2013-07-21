from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class WolneEbooki(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'authors':('./author', ''),
        'title':('./title', ''),
        'price':('./cena', 0),
        'formats':('./formats', ''),
        'url':('./link', ''),
        'cover':('./okladka', ''),
    }

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)

    def create_id_from_url(self, dic):
        dic['external_id'] = int(dic['url'].split('/')[-1])

class WolneEbookiBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    #authors
    title = Column(Unicode(256))         #42
    price = Column(Integer)              #GROSZE!!!
    url = Column(Unicode(64))            #35
    cover = Column(Unicode(64))          #38
