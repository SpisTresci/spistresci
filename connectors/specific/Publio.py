from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Publio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('./id', ''),
        'title':('./title', ''),
        'authors':('./authors', ''),
        'formats':('./formats', ''),
        'protectionType':('./protectionType', ''),  #???
        'price':('./price', ''),
        'url':('./productUrl', ''),
        'cover':('./imageUrl', ''),
        'isbns':('./isbns', ''),
        'publisher':('./company', ''),
        'categories':('./categories/category', ''),
    }

Base = SqlWrapper.getBaseClass()

class PublioBook(GenericBook, Base):
    #external_id
    title = Column(Unicode(256))
    #authors
    #formats
    #price
    url = Column(Unicode(256))
    cover = Column(Unicode(512))
    #isbns
    publisher = Column(Unicode(128))

    #protectionType - TODO T331
    #categories - TODO T334
