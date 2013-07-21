from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Czytio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', None),
        'title': ('./title', ''),
        'url': ('./url', ''),
        'authors': ('./authors', ''),
        'formats': ('./format', ''),
        'isbns': ('./isbn', ''),
        'cover': ('./cover', ''),
        'price': ('./price', 0),
        'size': ('./size', 0),
    }

Base = SqlWrapper.getBaseClass()

class CzytioBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    #title
    url = Column(Unicode(120))          #109
    #authors
    cover = Column(Unicode(128))        #118
    price = Column(Integer)             #GROSZE!!!
    size = Column(Integer)              #GROSZE!!!
