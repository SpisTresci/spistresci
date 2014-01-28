from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class BooksOn(Ceneo):

    xmls_namespace = {"n" : "http://www.w3.org/2001/XMLSchema-instance"}

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id',  ''),
        'price': ('@price', 0),
        'url': ('@url',  ''),
        'availability': ('@avail', ''),
        'set': ('@set', 0), #???
        'baset': ('@baset', 0), #???
        'category': ('./n:cat', ''),
        'title': ('./n:name', ''),
        'cover': ('./n:imgs/n:main/@url', ''),
        'description': ('./n:desc', ''),
        'authors': ("./n:attrs/n:a[@name='Autor']", ''),
    }

class BooksOnBook(GenericBook, Base):

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(60))           #59
    availability = Column(Integer)      #0/1
    set = Column(Integer)               #1 - ???
    baset = Column(Integer)             # ???!
    category = Column(Unicode(10))      #7
    title = Column(Unicode(256))        #26
    cover = Column(Unicode(128))        #90
