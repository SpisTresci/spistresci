from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Zinamon(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './tytul':('title', ''),
        './url':('url', ''),
        './autorzy':('authors', ''),
        './format':('formats', ''),
        './okladka':('cover', ''),
        './cena':('price', ''),
        './id':('external_id', ''),
        './isbn':('isbns', ''),
        './kategorie':('category', ''),
        './zabezpieczenia':('protection', ''),
    }

Base = SqlWrapper.getBaseClass()

class ZinamonBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    title = Column(Unicode(265))        #207
    url = Column(Unicode(512))          #338
    #authors
    cover = Column(Unicode(64))         #38
    price = Column(Integer)             #grosze
    category = Column(Unicode(512))     #20
    protection = Column(Unicode(16))    #9
