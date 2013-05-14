from connectors.generic import *
from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class KodeksyWmp3(Ceneo):

    depth=0 
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        "@id":('external_id',''),
        "@price":('price', 0),
        "@url":('url',''),
        "./cat":('category',''),
        "./name":('title',''),
        "./imgs/main[@url]":('cover',''),
        "./desc":('description',''),
        "./attrs/a[@name='EAN']":('isbn',''),
    }

#{'category': 31, 'isbn': 0, 'description': 4261, 'title': 37, 'url': 180, 'price': 5, 'cover': 45, 'external_id': 6}
class KodeksyWmp3Book(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    category = Column(Unicode(64))	#31
    isbn = Column(Unicode(13))		#13
    title = Column(Unicode(64))     #37
    url = Column(Unicode(256))		#180
    cover = Column(Unicode(64))	    #45
    external_id = Column(Integer)
    price = Column(Integer)

