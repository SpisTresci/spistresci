from connectors.common import *
from sqlwrapper import *

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
        "./attrs/a[@name='ISBN']":('isbn', ''),
        "./attrs/a[@name='Rok_wydania']":('date', ''),
        "./attrs/a[@name='Producent']":('publisher', ''),
        "./attrs/a[@name='Format']":('format', ''),
    }

class eClictoBook(CeneoBook, Base):
    id = Column(Integer, primary_key=True)

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(512))          #
    availability = Column(Integer)      #2-"99"
    set = Column(Integer)               #1 - ???
    category = Column(Unicode(60))      #54
    format = Column(Unicode(80))        #71
    publisher = Column(Unicode(46))     #54
    weight = Column(Unicode(4))         #4 - ???
    title = Column(Unicode(256))        #26
    cover = Column(Unicode(64))         #55
    isbn = Column(Unicode(13))          #0

class eClictoBookDescription(CeneoBookDescription, Base):
    pass

class eClictoAuthor(CeneoAuthor, Base):
    pass

class eClictoBookPrice(CeneoBookPrice, Base):
    pass

class eClictoBooksAuthors(CeneoBooksAuthors, Base):
    pass

