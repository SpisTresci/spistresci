from connectors.generic import *
from connectors.Tools import notFilterableConnector
from sqlwrapper import *
from connectors.generic import GenericBook
from utils.compatibility import json
import urllib2
import os
import hashlib

Base = SqlWrapper.getBaseClass()

@notFilterableConnector
class WolneLektury(JSONConnector):
    supported_formats = ['xml', 'fb2', 'mobi', 'pdf', 'txt', 'epub']

    tag_dict = {
        'title' : ('title', ''),
        'url' :  ('url', ''),
        'cover' : ('cover', ''),
        'cover_thumb': ('thumbnail', ''),
        'author': ('authors', ''),
     }

    def get_book_name_from_url(self, book_url):
        (filename, ext) = os.path.split(self.filename)
        book_path = urllib2.urlparse.urlparse(book_url).path
        if book_path.endswith('/'):
            book_path = book_path[:-1]
        return os.path.split(book_path)[1]


    def _fetch_full_book_file(self, book):
        book_url = book[u'href']
        book_name = self.get_book_name_from_url(book_url)
        filename = '%s_%s' % (self.filename, book_name)
        full_filepath = self.downloadFile(book_url, filename)
        return full_filepath

    def fetchData(self, unpack = True):
        full_filepath = self.downloadFile()
        if self.mode != GenericConnector.BookList_Mode.MULTIPLE_JSON:
            raise WrongConnectorModeException('Incorrect mode %s for connector type %s' %
            (GenericConnector.BookList_Mode.to_str(self.mode), self.__class__.__name__))

        self.fetched_files.append(full_filepath)
        with open(full_filepath, 'rU') as json_file:
            book_list = json.load(json_file)
        for book in book_list:
            self.fetched_files.append(self._fetch_full_book_file(book))

    #external id for wolnelektury is a md5 of url.
    #We believe url to boom is most stable
    def create_id_from_url(self, dic):
        dic['external_id'] = unicode(hashlib.md5(urllib2.urlparse.urlparse(dic['url']).path).hexdigest())


    def validate_number_of_books_in_db(self):
        session = sessionmaker(bind = SqlWrapper.getEngine())()
        db_count = session.query(WolneLekturyBook).count()
        session.close()

        book_list_len = len(self.book_list)
        if db_count < book_list_len:
            self.erratum_logger.error('Number of books in database (%d) is less than number got from connector (%d). Check it')
        elif db_count > book_list_len:
            self.erratum_logger.warning('Number of books in database (%d) is greater than number got from connector (%d). It is possible that some book exists in db twice')

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)

    def after_parse(self):
        self.validate_number_of_books_in_db()

    def parse(self):
        self.save_time_of_("parse_start")
        self.before_parse()
        book_number = 0
        with open(self.fetched_files[0], 'rU') as json_file:
            self.book_list = json.load(json_file)
        for book in self.book_list:
            book_name = self.get_book_name_from_url(book[u'href'])
            with open('%s_%s' % (self.fetched_files[0], book_name), 'rU') as json_file:
                book_details = json.load(json_file)
            book.update(book_details)

            dic = self.makeDict(book)
            self.adjust_parse(dic)
            #uncomment when creating connector
            #self.measureLenghtDict(dic)
            #print dic

            self.validate(dic)
            #comment out when creating connector
            self.add_record(dic)

        self.after_parse()
        #uncomment when creating connector
        #print self.max_len
        #print self.max_len_entry

        self.save_info_about_offers(offers_parsed = len(self.book_list))
        self.save_time_of_("parse_end")

    def validateFormats(self, dic, id, title):
        formats = [f for f in self.supported_formats if dic.get(f, None)]
        dic['formats'] = formats

#TODO: add external_id book model
class WolneLekturyBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
#    {'url': 121, 'cover': 125, 'thumbnail': 77, 'title': 91 }
    #price - derived
    external_id = Column(Unicode(32), unique = True)
    url = Column(Unicode(256))           #121
    title = Column(Unicode(128))        #91
    cover = Column(Unicode(256))        #125
    thumbnail = Column(Unicode(128))    #77
    #authors - derived

