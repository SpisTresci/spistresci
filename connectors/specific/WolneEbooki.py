import os
from connectors.generic import *
from xml.etree import ElementTree as et
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


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
	    #print dic
            self.validate(dic)
            #self.measureLenghtDict(dic)
            #self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])




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

