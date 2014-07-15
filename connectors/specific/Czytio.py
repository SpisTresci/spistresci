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
        'file_size': ('./size', 0),
        'page_count' : ('./length', 0),
    }

Base = SqlWrapper.getBaseClass()

class CzytioBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    #title
    #url
    #authors
    #cover
    price = Column(Integer)             #GROSZE!!!
    file_size = Column(Integer)
    page_count = Column(Integer)           
