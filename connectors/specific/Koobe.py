import os
from connectors.generic import *
from xml.etree import ElementTree as et
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Koobe(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./name":('title', ''),
        "./id":('external_id', ''),
        "./url":('url', ''),
        "./description":('description', ''),
        "./image":('cover', ''),
        "./price":('price', ''),
        "./category":('category', ''),
        "./producer":('publisher', ''),
        "./property[@name='isbn']":('isbn', ''),
        "./property[@name='author']":('authors', ''),
        "./property[@name='format']":('format', ''),
        "./property[@name='protection']":('protection', ''),
    }

    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root[0])
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
            #print dic
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key + ": " + unicode(self.max_len_entry[key])


class KoobeBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(256))		#202
    category = Column(Unicode(32))		#17
    publisher = Column(Unicode(64))     #57
    url = Column(Unicode(512))			#271
    #description
    isbn = Column(Unicode(13))			#13
    price = Column(Integer)		        #grosze
    cover = Column(Unicode(256))	    #159
    format = Column(Unicode(16))        #14
    protection = Column(Unicode(16))    #9

class KoobeBookDescription(GenericBookDescription, Base):
    pass

class KoobeAuthor(GenericAuthor, Base):
    pass

class KoobeBookPrice(GenericBookPrice, Base):
    pass

class KoobeBooksAuthors(GenericBooksAuthors, Base):
    pass

