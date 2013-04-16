from xml.etree import ElementTree as et
from connectors.generic import *
import os
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()
class Woblink(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        ".[@id]":('external_id', ''),
        ".[@price]":('price', 0),
        ".[@url]":('url', ''),
        ".[@avail]":('availability', ''),
        "./cat":('category', ''),
        "./name":('title', ''),
        "./imgs/main[@url]":('cover', ''),
        "./desc":('description', ''),
        "./attrs/a[@name='ISBN']":('isbn', ''),
        "./attrs/a[@name='Wydawnictwo']":('publisher', ''),
        "./attrs/a[@name='Format']":('formats', ''),
    }


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        print filename
        root = et.parse(filename).getroot()
        offers = list(root[0])
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
	#    try:
        #        print key+": "+ unicode(self.max_len_entry[key])
	#    except UnicodeEncodeError:
	#        pass


class WoblinkBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    category = Column(Unicode(64))	#33
    publisher = Column(Unicode(64))     #32
    isbn = Column(Unicode(13))		#13
    title = Column(Unicode(256))	#212
    url = Column(Unicode(64))		#59
    cover = Column(Unicode(256))	#250
    formats = Column(Unicode(16))	#9
    external_id = Column(Integer)
    price = Column(Integer)
    availability = Column(Boolean)
    pass

class WoblinkBookDescription(GenericBookDescription, Base):
    pass

class WoblinkAuthor(GenericAuthor, Base):
    pass

class WoblinkBookPrice(GenericBookPrice, Base):
    pass

class WoblinkBooksAuthors(GenericBooksAuthors, Base):
    pass
