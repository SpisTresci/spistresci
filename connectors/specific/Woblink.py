from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()
class Woblink(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id', ''),
        'price': ('@price', 0),
        'url': ('@url', ''),
        'availability': ('@avail', ''),
        'category': ('./cat', ''),
        'title': ('./name', ''),
        'cover': ('./imgs/main/@url', ''),
        'description': ('./desc', ''),
        'isbns': ("./attrs/a[@name='ISBN']", ''),
        'publisher': ("./attrs/a[@name='Wydawnictwo']", ''),
        'formats': ("./attrs/a[@name='Format']", ''),
    }

class WoblinkBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    category = Column(Unicode(64))      #33
    publisher = Column(Unicode(64))     #32
    title = Column(Unicode(256))        #212
    url = Column(Unicode(64))           #59
    cover = Column(Unicode(256))        #250
    price = Column(Integer)
    availability = Column(Boolean)

