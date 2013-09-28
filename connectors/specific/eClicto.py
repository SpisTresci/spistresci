from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class eClicto(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id', ''),
        'url': ('@url', ''),
        'price': ('@price', 0),
        'set': ('@set', 0), #???
        'availability': ('@avail', ''),
        'weight': ('@weight', '0.00'),

        'category': ('./cat', ''),
        'title': ('./name', ''),
        'cover': ('./imgs/main/@url', ''),
        'description': ('./desc', ''),
        'authors': ("./attrs/a[@name='Autor']", ''),
        'isbns': ("./attrs/a[@name='ISBN']", ''),
        'date': ("./attrs/a[@name='Rok_wydania']", ''),
        'publisher': ("./attrs/a[@name='Producent']", ''),
        'formats': ("./attrs/a[@name='Format']", ''),
    }

class eClictoBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(512))          #
    availability = Column(Integer)      #2-"99"
    set = Column(Integer)               #1 - ???
    category = Column(Unicode(60))      #54
    publisher = Column(Unicode(46))     #54
    weight = Column(Unicode(4))         #4 - ???
    title = Column(Unicode(256))        #26
    cover = Column(Unicode(64))         #55

