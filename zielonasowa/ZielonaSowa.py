from afiliant import *
from sql_wrapper import *

import os
from generic import *
from xml.etree import ElementTree as et


Base = SqlWrapper.getBaseClass()

class ZielonaSowa(Afiliant):
    def parse(self):
        filename = os.path.join(self.backup_dir,self.filename)
        root = et.parse(filename).getroot()
        body = root[0]
        loadoffers = body[0]
        offerstag = loadoffers[0]
        offers=list(offerstag)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic
            self.validate(dic)
            self.mesureLenghtDict(dic)
            #print dic
            self.add_record(dic)

        print self.max_len
        for key in self.max_len_entry.keys():
            print key+": "+ unicode(self.max_len_entry[key])

class ZielonaSowaBook(AfiliantBook, Base):
    id =  Column(Integer, primary_key=True)

    category = Column(Unicode(90))      #82
    #title(255)                         #82
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(120))        #115
    #lectors
    manufacturer = Column(Unicode(70)) #63

class ZielonaSowaBookDescription(AfiliantBookDescription, Base):
    pass

class ZielonaSowaAuthor(AfiliantAuthor, Base):
    pass

class ZielonaSowaBookPrice(AfiliantBookPrice, Base):
    pass

class ZielonaSowaBooksAuthors(AfiliantBooksAuthors, Base):
    pass