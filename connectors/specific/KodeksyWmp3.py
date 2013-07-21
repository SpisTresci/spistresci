from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class KodeksyWmp3(Ceneo):

    depth = 0
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id', ''),
        'price': ('@price', 0),
        'url': ('@url', ''),
        'category': ('./cat', ''),
        'title': ('./name', ''),
        'cover': ('./imgs/main[@url]', ''),
        'description': ('./desc', ''),
        'isbns': ("./attrs/a[@name='EAN']", ''),
    }

#{'category': 31, 'isbn': 0, 'description': 4261, 'title': 37, 'url': 180, 'price': 5, 'cover': 45, 'external_id': 6}
class KodeksyWmp3Book(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    category = Column(Unicode(64))      #31
    title = Column(Unicode(64))         #37
    url = Column(Unicode(256))          #180
    cover = Column(Unicode(64))         #45
    price = Column(Integer)


