from connectors.generic import *
from connectors.common import *
from connectors.Tools import notFilterableConnector
from sqlwrapper import *
from utils.compatibility import json
import urllib2
import os

Base = SqlWrapper.getBaseClass()

@notFilterableConnector
class WolneLektury(JSONConnector):
    possible_formats = ['xml', 'fb2', 'mobi', 'pdf', 'txt', 'epub']
    def get_book_name_from_url(self, book_url):
        (filename, ext) = os.path.split(self.filename)
        book_path = urllib2.urlparse.urlparse(book_url).path
        if book_path.endswith('/')
            book_path = book_path[:-1]
        book_name = os.path.split(book_path)[1]

    def _fetch_full_book_file(self, book):
        book_name = self.get_book_name_from_url(book[u'href'])
        filename = '%s_%s' % (self.filename, book_name)
        full_filepath = self.downloadFile(book_url, filename)
        return full_filepath
    
    def fetchData(self, unpack=True):
        full_filepath = self.downloadFile()
        if self.mode != GenericConnector.BookList_Mode.MULTIPLE_JSON:
            raise WrongConnectorModeException('Incorrect mode %s for connector type %s' % 
            (GenericConnector.BookList_Mode.to_str(self.mode), self.__class__.__name__))

        self.fetched_files.append(full_filepath)

        book_list = json.loads(full_filepath)
        for book in book_list:
            self.fetched_file.append(self._fetch_full_book_file(book))

    def parse(self):
        self.before_parse()
        book_number = 0
        book_list = json.load(self.fetched_files[0])
        for book in book_list:
            book_name = self.get_book_name_from_url(book[u'href'])
            book_details = json.load('%s_%s' % (self.fetched_files[0], book_name))
            book.update(book_details)
            formats = [f for f in self.possible_formats if book.get(f,None)]
            book['formats'] = formats
            
#TODO: adjust book model
class WolneLekturyBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
#    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(256))           #152
    title = Column(Unicode(256))        #136
    cover = Column(Unicode(128))        #118
    authors = Column(Unicode(128))

