from connectors.generic import *
from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()
class Woblink(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "@id":('external_id', ''),
        "@price":('price', 0),
        "@url":('url', ''),
        "@avail":('availability', ''),
        "./cat":('category', ''),
        "./name":('title', ''),
        "./imgs/main[@url]":('cover', ''),
        "./desc":('description', ''),
        "./attrs/a[@name='ISBN']":('isbns', ''),
        "./attrs/a[@name='Wydawnictwo']":('publisher', ''),
        "./attrs/a[@name='Format']":('formats', ''),
    }

class WoblinkBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    category = Column(Unicode(64))	#33
    publisher = Column(Unicode(64))     #32
    title = Column(Unicode(256))	#212
    url = Column(Unicode(64))		#59
    cover = Column(Unicode(256))	#250
    external_id = Column(Integer)
    price = Column(Integer)
    availability = Column(Boolean)

