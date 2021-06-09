from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Koobe(XMLConnector):

    depth = 1
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'title': ('./name', ''),
        'external_id': ('./id', ''),
        'url': ('./url', ''),
        'description': ('./description', ''),
        'cover': ('./image', ''),
        'price': ('./price', ''),
        'category': ('./category', ''),
        'publisher': ('./producer', ''),
        'isbns': ("./property[@name='isbn']", ''),
        'authors': ("./property[@name='author']", ''),
        'formats': ("./property[@name='format']", ''),
        'protection': ("./property[@name='protection']", ''),
    }

class KoobeBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(256))        #202
    category = Column(Unicode(32))      #17
    publisher = Column(Unicode(64))     #57
    #url
    #description
    price = Column(Integer)             #grosze
    #cover
    protection = Column(Unicode(16))    #9
