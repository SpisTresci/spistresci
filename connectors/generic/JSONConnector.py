from connectors.generic import GenericConnector
from connectors.generic import WrongConnectorModeException
from utils.compatibility import json
import os

class JSONConnector(GenericConnector):

    skip_offers = 0

    def __init__(self, name=None, limit_books=0):
        GenericConnector.__init__(self, name=name)
        self.limit_books = limit_books

    def fetchData(self, unpack=True):
        self.downloadFile()
        #TODO: this definatelly should not be here ..... or... let's not use 'definatelly' here
        if GenericConnector.BookList_Mode.to_str(self.mode).endswith('XML') or GenericConnector.BookList_Mode.to_str(self.mode).endswith('XMLS'):
            raise WrongConnectorModeException('Incorrect mode %s for connector type %s' % 
            (GenericConnector.BookList_Mode.to_str(self.mode), self.__class__.__name__))
        elif unpack and self.mode == GenericConnector.BookList_Mode.ZIPPED_JSON:
            self.fetched_files.extend(
              self.unpackZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif unpack and self.mode == GenericConnector.BookList_Mode.GZIPPED_JSON:
            self.fetched_files.extend(
              self.unpackGZIP(os.path.join(self.backup_dir, self.filename))
            )
        elif self.mode == GenericConnector.BookList_Mode.SINGLE_JSON:
            self.fetched_files.append(os.path.join(self.backup_dir, self.filename))

    def parse(self):
        self.before_parse()
        book_number = 0
        for filename in self.fetched_files:
            json_file=open(filename, 'rU')
            book_list = json.loads(json_file.read())
            for book in book_list:
                book_number += 1
                if book_number < self.skip_offers + 1:
                    continue
                elif self.limit_books and book_number > self.limit_books:
                    break
                self.adjust_parse(book)
                self.validate(book)
                #uncomment when creating connector
                self.measureLenghtDict(book)
                #print book
                #comment out when creating connector
                #self.add_record(book)

        self.after_parse()
        #uncomment when creating connector
        print self.max_len
        print self.max_len_entry
