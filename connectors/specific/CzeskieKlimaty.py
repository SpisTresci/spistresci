from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class CzeskieKlimaty(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ("@id", ''),
        'price': ("@price",  0),
        'url': ("@url", ''),
        'title': ("./name", ''),
        'description': ("./desc", ''),
        'category': ("./cat", ''),
        'cover': ("./imgs/main[@url]", ''),
        'authors': ("./attrs/a[@name='Autor']", ''),
        'isbns': ("./attrs/a[@name='ISBN']", ''),
        'page_count': ("./attrs/a[@name='Ilosc_stron']", ''),
        'publisher': ("./attrs/a[@name='Wydawnictwo']", ''),
        'date': ("./attrs/a[@name='Rok_wydania']", ''),
    }


class CzeskieKlimatyBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(80))           #59

    title = Column(Unicode(256))        #143
    #description
    category = Column(Unicode(80))      #72
    cover = Column(Unicode(64))         #38
    #authors
    #isbns
    page_count = Column(Integer)
    publisher = Column(Unicode(70))     #59
    date = Column(Date)                 #
