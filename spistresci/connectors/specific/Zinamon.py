from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Zinamon(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'title': ('./tytul', ''),
        'url': ('./url', ''),
        'authors': ('./autorzy', ''),
        'formats': ('./format', ''),
        'cover': ('./okladka', ''),
        'price': ('./cena', ''),
        'external_id': ('./id', ''),
        'isbns': ('./isbn', ''),
        'category': ('./kategorie', ''),
        'protection': ('./zabezpieczenia', ''),
    }

Base = SqlWrapper.getBaseClass()

class ZinamonBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    external_id = Column(Unicode(16), unique=True)
    title = Column(Unicode(265))        #207
    #url
    #authors
    #cover
    price = Column(Integer)             #grosze
    category = Column(Unicode(512))     #20
    protection = Column(Unicode(16))    #9
