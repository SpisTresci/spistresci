from connectors.generic import *
from sqlwrapper import *
import os
import xml.etree.ElementTree as et

Base = SqlWrapper.getBaseClass()

class FantastykaPolska(XMLConnector):

    depth = 1
    skip_offers = 4

    author_class_name='field field-name-field-autor field-type-taxonomy-term-reference field-label-inline inline clearfix'
    notes_class_name='field field-name-field-uwagi field-type-text field-label-inline inline'
    category_class_name='field field-name-field-kategoria field-type-taxonomy-term-reference field-label-inline inline clearfix'
    genre_class_name='field field-name-field-gatunek field-type-taxonomy-term-reference field-label-inline inline clearfix'
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./title":('title', ''),
        "./filteredId":('external_id', ''),
        "./link":('url', ''),
        "./description/div[@class='%s']/ul/li/a"%author_class_name:('authors', ''),
        "./description/div/div[@class='field-items']/div":('notes', ''),
        "./description/div[@class='%s']/ul/li/a"%category_class_name:('category', ''),
        "./description/div[@class='%s']/ul/li/a"%genre_class_name:('genre', ''),
    }

class FantastykaPolskaBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(64))        #44
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(64))          #50
    category = Column(Unicode(16))      #11
    notes = Column(Unicode(32))         #22
    genre = Column(Unicode(32))         #29
    external_id = Column(Integer)
