from connectors.generic import *
from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class BooksOn(Ceneo):
    
    xmls_namespace = {"n" : "http://www.w3.org/2001/XMLSchema-instance"} 
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        "@id":('external_id',''),
        "@price":('price', 0),
        "@url":('url',''),
        "@avail":('availability',''),
        "@set":('set', 0), #???
        "@baset":('baset', 0), #???
        "./n:cat":('category',''),
        "./n:name":('title',''),
        "./n:imgs/n:main[@url]":('cover',''),
        "./n:desc":('description',''),
        "./n:attrs/n:a[@name='Autor']":('authors',''),
    }

class BooksOnBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(60))           #59
    availability = Column(Boolean)      #0/1
    set = Column(Integer)               #1 - ???
    baset = Column(Integer)             # ???!
    category = Column(Unicode(10))      #7
    title = Column(Unicode(256))        #26
    cover = Column(Unicode(128))        #90
    isbn = Column(Unicode(13))          #0
