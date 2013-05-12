from connectors.generic import XMLConnector
from connectors.generic import *
from sqlwrapper import *
import lxml.etree as et
import os
import urllib, urllib2

class TaniaKsiazka(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "@awId":('awId', ''),
        "@programName":('programName', ''),
        './pId':('external_id', None),
        './name':('title', ''),
        './desc':('description', ''),
        './cat/awCatId':('category_id', ''),
        './cat/awCat':('category', ''),
        './cat/mCat':('type', ''),
        './brand':('brand', ''),
        './awLink':('url', ''),
        './awThumb':('thumbnail', ''),
        './awImage':('cover', ''),
        "./price/display":('price', 0),
        "./atribute[@Name='ISBN']":('isbn', ''),
       }

Base = SqlWrapper.getBaseClass()

class TaniaKsiazkaBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    category = Column(Unicode(32))          #22
    isbn = Column(Unicode(13))              #13
    title = Column(Unicode(256))            #200
    url = Column(Unicode(512))              #284
    type = Column(Unicode(64))              #51
    price = Column(Integer)                 #grosze
    cover = Column(Unicode(64))             #46
    thumbnail = Column(Unicode(64))         #47
    programName = Column(Unicode(32))       #16
    category_id = Column(Integer)           #
    brand = Column(Unicode(32))             #?
    awId = Column(Integer)                  #

