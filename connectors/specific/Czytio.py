from connectors.generic import *
import lxml.etree as et
import urllib2
import os
from sqlwrapper import *

class Czytio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './id':('external_id', None),
        './title':('title', ''),
        './url':('url', ''),
        './authors':('authors', ''),
        './format':('format', ''),
        './isbn':('isbn', ''),
        './cover':('cover', ''),
        './price':('price', 0),
        './size':('size', 0),
    }

Base = SqlWrapper.getBaseClass()

class CzytioBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    #title
    url = Column(Unicode(120))          #109
    #authors
    format = Column(Unicode(4))         #4
    isbn = Column(Unicode(25))          #20, 978-83-02-63935-07-8
    cover = Column(Unicode(128))        #118
    price = Column(Integer)             #GROSZE!!!
    size = Column(Integer)             #GROSZE!!!
