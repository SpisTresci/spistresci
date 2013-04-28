import os
from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class WolneEbooki(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./author":('authors', ''),
        "./title":('title', ''),
        "./cena":('price', 0),
        "./formats":('format', ''),
        "./link":('url', ''),
        "./okladka":('cover', ''),
    }

    def validate(self, dic):
        self.create_id_from_url(dic)
        super(WolneEbooki, self).validate(dic)

    def create_id_from_url(self, dic):
        dic['external_id'] = int(dic['url'].split('/')[-1])

class WolneEbookiBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    #authors
    title = Column(Unicode(256))         #42
    price = Column(Integer)              #GROSZE!!!
    format = Column(Unicode(32))         #15
    url = Column(Unicode(64))            #35
    cover = Column(Unicode(64))          #38

class WolneEbookiBookDescription(GenericBookDescription, Base):
    pass

class WolneEbookiAuthor(GenericAuthor, Base):
    pass

class WolneEbookiBookPrice(GenericBookPrice, Base):
    pass

class WolneEbookiBooksAuthors(GenericBooksAuthors, Base):
    pass

