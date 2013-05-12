import os
from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

class BezKartek(XMLConnector):

    depth = 1
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './isbn':('isbn', ''),
        './ebookId':('external_id', None),
        './name':('title', ''),
        './url':('url', None),
        './authors':('authors', ''),
        './category':('category', ''),
        './description':('description', ''),
        './format':('format', ''),
        './image':('cover', ''),
        './languages/lang_short':('lang_short', ''),
        './languages/lang_long': ('lang_long', ''),
        './price':('price', 0),
        './pageCount':('page_count', 0),
        './publisher':('publisher', ''),
        './securityType':('security', ''),
        './audioTime':('audio_time', ''),
    }

Base = SqlWrapper.getBaseClass()

class BezKartekBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

    category = Column(Unicode(30))      #29

    audio_time = Column(Unicode(10))    #9
    isbn = Column(Unicode(30))          #27, 978-83-63444-25-9/1895-247X
    format = Column(Unicode(4))         #4
    price = Column(Integer)             #GROSZE!!!
    page_count = Column(Integer)        #508700 - wtf?
    publisher = Column(Unicode(70))     #68
    url = Column(Unicode(270))          #265
    cover = Column(Unicode(256))        #184
    security = Column(Unicode(10))      #9
    lang_short = Column(Unicode(2))     #2
    lang_long = Column(Unicode(10))     #9
