from connectors.generic import XMLConnector
from xml.etree import ElementTree as et
from connectors.generic import *
import os
import re

class Ceneo(XMLConnector):

    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        group_books = root[0]
        offers = list(group_books)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])


class CeneoBook(GenericBook):
    pass

class CeneoBookDescription(GenericBookDescription):
    pass

class CeneoAuthor(GenericAuthor):
    pass

class CeneoBookPrice(GenericBookPrice):
    pass

class CeneoBooksAuthors(GenericBooksAuthors):
    pass
