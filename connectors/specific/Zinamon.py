from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

class Zinamon(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './tytul':('title', ''),
        './url':('url', ''),
        './autorzy':('authors', ''),
        './format':('format', ''),
        './okladka':('cover', ''),
        './cena':('price', ''),
        './id':('external_id', ''),
        './isbn':('isbn', ''),
        './kategorie':('category',''),
        './zabezpieczenia':('protection',''),
    }

Base = SqlWrapper.getBaseClass()

class ZinamonBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

    title = Column(Unicode(265))        #207
    url = Column(Unicode(512))          #338
    #authors
    format = Column(Unicode(8))         #4
    cover = Column(Unicode(64))         #38
    price = Column(Integer)             #grosze
    external_id = Column(Unicode(16))   #10
    isbn = Column(Unicode(13))          #0
    category = Column(Unicode(512))     #20
    protection = Column(Unicode(16))    #9

class ZinamonBookDescription(GenericBookDescription, Base):
    pass

class ZinamonAuthor(GenericAuthor, Base):
    pass

class ZinamonBookPrice(GenericBookPrice, Base):
    pass

class ZinamonBooksAuthors(GenericBooksAuthors, Base):
    pass
