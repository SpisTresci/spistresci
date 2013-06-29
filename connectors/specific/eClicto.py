from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class eClicto(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "@id":('external_id', ''),
        "@url":('url', ''),
        "@price":('price', 0),
        "@set":('set', 0), #???
        "@avail":('availability', ''),
        "@weight":('weight', '0.00'),

        "./cat":('category', ''),
        "./name":('title', ''),
        "./imgs/main[@url]":('cover', ''),
        "./desc":('description', ''),
        "./attrs/a[@name='Autor']":('authors', ''),
        "./attrs/a[@name='ISBN']":('isbns', ''),
        "./attrs/a[@name='Rok_wydania']":('date', ''),
        "./attrs/a[@name='Producent']":('publisher', ''),
        "./attrs/a[@name='Format']":('formats', ''),
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

