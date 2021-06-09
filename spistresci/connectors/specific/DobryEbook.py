from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class DobryEbook(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'title': ('./tytul', ''),
        'subtitle': ('./podtytul', ''),
        'authors': ('./autor', ''),
        'url': ('./link', ''),
        'price': ('./cena', ''),
        'file_size': ('./wielkosc_pliku', ''),
        'page_count': ('./liczba_stron', ''),
        'isbns': ('./isbn', ''),
        'cover_small': ('./male_zdjecie', ''),
        'cover': ('./duze_zdjecie', ''),
    }

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)
        #DobryEbook has only pdf books
        dic['formats'] = ['pdf']

    def create_id_from_url(self, dic):
        dic['external_id'] = int(dic['url'].split("-")[-1].split(".")[0])

class DobryEbookBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(256))            #101
    subtitle = Column(Unicode(128))         #70

    #url
    page_count = Column(Integer)            #Integer
    #cover
    cover_small = Column(STUrl)     #128
    file_size = Column(Unicode(16))         #8

