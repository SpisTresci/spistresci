from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class CzeskieKlimaty(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        ".[@id]":('external_id', ''),
        ".[@price]":('price', 0),
        ".[@url]":('url', ''),

        "./name":('title', ''),
        "./desc":('description', ''),
        "./cat":('category', ''),
        "./imgs/main[@url]":('cover', ''),
        "./attrs/a[@name='Autor']":('authors', ''),
        "./attrs/a[@name='ISBN']":('isbn', ''),
        "./attrs/a[@name='Ilosc_stron']":('page_count', ''),
        "./attrs/a[@name='Wydawnictwo']":('publisher', ''),
        "./attrs/a[@name='Rok_wydania']":('date', ''),
    }


class CzeskieKlimatyBook(CeneoBook, Base):
    id = Column(Integer, primary_key=True)

    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(80))           #59

    title = Column(Unicode(256))        #143
    #description
    category = Column(Unicode(80))      #72
    cover = Column(Unicode(64))         #38
    #authors
    isbn = Column(Unicode(13))          #
    page_count = Column(Integer)
    publisher = Column(Unicode(70))     #59
    date = Column(Date)                 #





class CzeskieKlimatyBookDescription(CeneoBookDescription, Base):
    pass

class CzeskieKlimatyAuthor(CeneoAuthor, Base):
    pass

class CzeskieKlimatyBookPrice(CeneoBookPrice, Base):
    pass

class CzeskieKlimatyBooksAuthors(CeneoBooksAuthors, Base):
    pass

