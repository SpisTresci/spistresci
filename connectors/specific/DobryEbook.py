import os
from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class DobryEbook(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./tytul":('title', ''),
        "./podtytul":('subtitle', ''),
        "./autor":('authors', ''),
        "./link":('url', ''),
        "./cena":('price', ''),
        "./wielkosc_pliku":('file_size', ''),
        "./liczba_stron":('page_count', ''),
        "./isbn":('isbn', ''),
        "./male_zdjecie":('small_cover', ''),
        "./duze_zdjecie":('cover', ''),
    }

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)

    def create_id_from_url(self, dic):
        dic['external_id'] = int(dic['url'].split("-")[-1].split(".")[0])

class DobryEbookBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(256))		#101
    subtitle = Column(Unicode(128))		#70

    url = Column(Unicode(256))			#133
    isbn= Column(Unicode(13))			#13
    page_count = Column(Integer)		#Integer
    cover = Column(Unicode(64))			#60
    small_cover = Column(Unicode(64))		#60
    file_size = Column(Unicode(16))		#8
