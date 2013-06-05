import os
from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Koobe(XMLConnector):

    depth = 1
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./name":('title', ''),
        "./id":('external_id', ''),
        "./url":('url', ''),
        "./description":('description', ''),
        "./image":('cover', ''),
        "./price":('price', ''),
        "./category":('category', ''),
        "./producer":('publisher', ''),
        "./property[@name='isbn']":('isbns', ''),
        "./property[@name='author']":('authors', ''),
        "./property[@name='format']":('formats', ''),
        "./property[@name='protection']":('protection', ''),
    }

class KoobeBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(256))		#202
    category = Column(Unicode(32))		#17
    publisher = Column(Unicode(64))     #57
    url = Column(Unicode(512))			#271
    #description
    price = Column(Integer)		        #grosze
    cover = Column(Unicode(256))	    #159
    protection = Column(Unicode(16))    #9

