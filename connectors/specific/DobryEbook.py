import os
from connectors.generic import *
from xml.etree import ElementTree as et
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


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
            self.create_id_from_url(dic)
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key + ": " + unicode(self.max_len_entry[key])

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

class DobryEbookBookDescription(GenericBookDescription, Base):
    pass

class DobryEbookAuthor(GenericAuthor, Base):
    pass

class DobryEbookBookPrice(GenericBookPrice, Base):
    pass

class DobryEbookBooksAuthors(GenericBooksAuthors, Base):
    pass

