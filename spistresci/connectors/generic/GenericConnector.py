# -*- coding: utf-8 -*-
import urllib2
import zipfile
import tarfile
import gzip
import bz2
import os.path
import shutil
import re
from datetime import datetime
import base64
import time

import ConfigParser
from spistresci.connectors.utils.ConnectorsLogger import logger_instance
from spistresci.connectors.utils.DataValidator import DataValidator
from spistresci.connectors.utils import MultiLevelConfigParser
from spistresci.connectors.utils.EnumMeta import Enum
from spistresci.connectors.utils.GetOrCreateCache import GetOrCreateCache
#from sqlalchemy.ext.associationproxy import association_proxy
#from sqlalchemy.orm import class_mapper
import spistresci.connectors.utils
#interesting thing: utils.Enum is hide by sql_wrapper.Enum
#from sqlwrapper import *
from spistresci.connectors import Tools
#from models import *
from spistresci.connectors.utils.ConfigReader import ConfigReader
from django.conf import settings


#Base = SqlWrapper.getBaseClass()
from spistresci.model_controler import add_MiniBook
from spistresci.models import Bookstore, BookstoreCommandStatus


class InvalidContext(RuntimeError):
    pass

class WrongConnectorModeException(RuntimeError):
    pass

class GenericBase(object):

    registered = {}

    @classmethod
    def register(cls):
        if not cls.__name__ in cls.registered:
            cls.registered[cls.__name__] = cls

    @staticmethod
    def getConcretizedClass(context, className):
        if not isinstance(context, GenericBase):
            raise InvalidContext("Only not abstract classes that inherit from GenericBase cat use this method")

        for name in ['Author', 'Book', 'BooksAuthors', 'ISBN', 'Format', 'UpdateStatus']:
            if context.name.endswith(name):
                return GenericBase.registered[context.name[:-len(name)] + className]
        else: #Connector
            return GenericBase.registered[context.name + className]

class GenericConnector(GenericBase, DataValidator):

    '''
    NONE - remove backup dir after execution
    UNCOMPRESSED - do not touch backup dir after execution
    BZIP - create tar.bz2 archive
    GZIP - create tar.gz archive
    '''
    class ArchiveType(Enum):
        values = ['NONE', 'UNCOMPRESSED', 'BZIP', 'GZ']

    class InnerMerge(Enum):
        values = ['NONE', 'ALL', 'GROUP']

    class BookList_Mode(Enum):
        values = [
            'UNKNOWN',

            'SINGLE_XML',
            'ZIPPED_XMLS',
            'GZIPPED_XMLS',
            'BZIPPED_XMLS',
            'MULTIPLE_XMLS',

            'SINGLE_JSON',
            'ZIPPED_JSON',
            'GZIPPED_JSON',
            'BZIPPED_JSON',
            'MULTIPLE_JSON',
        ]

    max_len = {}
    max_len_entry = {}

    config_file = 'update.ini'
    config_object = None

    rows_initialized = True#False
    skip_offers = 0

    session_obj_limit = 1000

    @classmethod
    def class_name(cls):
        return cls.__name__

    @property
    def name(self):
        return self._name

    def __init__(self, name=None, limit_books=0):
        if not name:
            self._name = self.class_name()
        else:
            self._name = name
        self.limit_books = limit_books
        self.register()
        self.config_object = ConfigReader.read_config(self.config_file)
        self.config = ConfigReader.parse_config(config_object=self.config_object, section = self.name, vars= {'date':datetime.now().strftime('%Y%m%d%H%M%S'),
                                                                         'connector_lowcase':self.name.lower(),
                                                                         'connector':self.name})
        self.url = self.config['url']
        self.port = self.config.get('port', '')
        self.database_name = self.config.get('database_name', '')
        self.preferred_record_syntax = self.config.get('preferred_record_syntax', '')
        self.filename = self.config['filename']
        self.backup_dir = self.config.get('backup_dir', '')
        self.backup_archive = self.ArchiveType.int(self.config.get('backup_archive', 'NONE'))
        self.unpack_file = self.config.get('unpack_file', '')
        self.unpack_dir = self.config.get('unpack_dir', '')
        self.remove_unpacked = int(self.config.get('remove_unpacked', 1))
        self.log_config = self.config.get('log_config', 'log.update.ini')
        self.logger = logger_instance(os.path.join(settings.SITE_ROOT, self.log_config))
        self.log_erratum_config = self.config.get('log_erratum_config', 'conf/log.erratum.ini')
        self.erratum_logger = logger_instance(os.path.join(settings.SITE_ROOT, self.log_erratum_config))
        self.logger.debug('%s connector created' % self.name)
        self.mode = self.BookList_Mode.int(self.config.get('mode', 'UNKNOWN'))
        self.filters_config = self.config.get('filters', {})
        self.fulfill = self.config.get('fulfill')
        self.pp_url = self.config.get('pp_url')
        self.password = self.config.get('password')
        self.username = self.config.get('username')
        self.inner_merge = self.InnerMerge.int(self.config.get('inner_merge', 'NONE'))
        if type(self.filters_config) is dict:
            self.filters = self.filters_config.get('')
        else:
            self.filters = self.filters_config
            self.filters_config = {}
        self.fetched_files = []
        self.update_status_service = None
        self.loadListOfNames()
        self.session_obj_counter = 0
        self.bookstore, created = Bookstore.objects.get_or_create(
            name=self.name,
            url=self.url,
        )

    def __del__(self):
        if self.logger:
            self.logger.debug('Cleaning up after executing %s connector' % self.name)
        if self.backup_dir:
            if self.backup_archive in [self.ArchiveType.BZIP, self.ArchiveType.GZ] and \
               self.mode not in [self.BookList_Mode.ZIPPED_XMLS, self.BookList_Mode.GZIPPED_XMLS, self.BookList_Mode.BZIPPED_XMLS]:
                self.compress_dir(self.backup_dir, self.backup_archive)
                self.backup_archive = self.ArchiveType.NONE

            if self.backup_archive == self.ArchiveType.NONE and os.path.exists(self.backup_dir):
                self._rm_ifpossible(self.backup_dir, 'backup')
                self.backup_dir = ''

        if self.unpack_dir and self.remove_unpacked and os.path.exists(self.unpack_dir):
            self._rm_ifpossible(self.unpack_dir, 'unpack')
            self.unpack_dir = ''

    def _rm_ifpossible(self, path, dir_type='backup'):
        cwd = os.getcwd().rstrip('/') + '/'
        abs_path = os.path.abspath(path).rstrip('/') + '/'
        if abs_path in cwd:
            raise IOError(
            'Are you insane or something?. Don\'t tell me to remove whole my working dir (%s). HINT:%s dir should not be current dir or parent' % (path, dir_type)
            )
        self.logger.debug('Connector %s. Removing %s dir %s' % (self.name, dir_type, path))
        shutil.rmtree(path)


    def compress_dir(self, path, archive_type):
        if archive_type == self.ArchiveType.GZ:
            mode = 'gz'
        else:
            mode = 'bz2'
        path = os.path.abspath(path)
        basename = os.path.basename(path)
        tar_name = os.path.abspath(os.path.join(path, '..' , '%s.tar.%s' % (basename, mode)))
        self.logger.debug('Comprassing dir %s to %s', path, tar_name)
        tar = tarfile.open(tar_name, 'w:%s' % mode)
        tar.add(path, arcname=basename)

    def decompress_backup_dir(self, path, archive_type):
        mode="r:"
        if archive_type == self.ArchiveType.GZ:
            mode += 'gz'
        else:
            mode += 'bz2'

        cwd = os.getcwd()
        dir  = os.path.dirname(path)
        basename = os.path.basename(path)

        os.chdir(dir)
        try:
            file = tarfile.open(basename, mode)
            try:
                file.extractall()
                for member in file.getmembers():
                    d = os.path.join(cwd, dir, member.path)
                    if os.path.isfile(d):
                        self.fetched_files.append(d)
            finally:
                file.close()
        finally:
            os.chdir(cwd)

        self.unpack_dir
        self.unpack_file


    def createSession(self):
        Session = sessionmaker(bind = SqlWrapper.getEngine())
        self.session = Session()

    def closeSession(self):
        self.session.commit()
        self.session.close()

    def fetchData(self):
        """fetchData method"""

        checksum = self.calculateChecksum()
        bcs = self.bookstore_cmd_status
        extra = dict(bcs.extra)
        extra['checksum'] = checksum
        bcs.extra = extra
        bcs.save()

    
    def getBookList(self, filename):
        pass

    def _parse_measure_length(self, adjust=True):

        book_number = 0
        for filename in self.fetched_files:
            for offer in self.getBookList(filename):
                book_number += 1
                if self.limit_books and book_number > self.limit_books:
                    break
                book = self.makeDict(offer)

                if adjust:
                    self.adjust_parse(book)

                self.measureLenghtDict(book)

        print self.max_len
        #print self.max_len_entry

    def _parse_make_test_dict(self, adjust=False):
        if adjust:
            self.before_parse()
        book_number = 0 
        for filename in self.fetched_files:
            for offer in self.getBookList(filename):
                book_number += 1
                if self.limit_books and book_number > self.limit_books:
                    break
                book = self.makeDict(offer)
                if adjust:
                    self.adjust_parse(book)
                print book
            if adjust:
                self.after_parse()


    def parse(self, force=False):
        #self.save_time_of_("parse_start")
        self.before_parse()
        book_number = 0
        force = True # TODO - REMOVE ASAP
        if self.areDataDifferentThanPrevious() or force:
            for filename in self.fetched_files:
                for offer in self.getBookList(filename):
                    book_number += 1
                    #TODO:remove skip_offer option,
                    #if necessary  override getBookList
                    if book_number < self.skip_offers + 1:
                        continue
                    elif self.limit_books and book_number > self.limit_books:
                        break
                    book = self.makeDict(offer)
                    self.adjust_parse(book)
                    #uncomment when creating connector
                    #print book

                    self.validate(book)
                    if self.fulfillRequirements(book):
                        self.create_pp_url(book)
                        self.new_add_record(book)
                        #self.add_record(book)

                    self.bookstore_cmd_status.feed_dog()

            self.after_parse()
            #self.session.commit()
            #self.save_info_about_offers(offers_parsed = book_number)
        else:
            pass
            #self.save_info_about_offers(offers_new = 0)

        #self.save_time_of_("parse_end")


    '''override before_parse, adjust_parse and after_parse to
        add some connector specific steps to parse method'''
    def before_parse(self):
        pass

    def adjust_parse(self, dic):
        pass

    def after_parse(self):
        pass

    def create_pp_url(self, book):
        if self.pp_url:
            my_book = book.copy()
            for x in my_book.keys():
                #this is pythonic way :)
                try:
                    val = my_book[x]
                    my_book[x] = re.sub(self.pp_url[x]['pattern'], self.pp_url[x]['replace'], val)
                except KeyError, TypeError:
                    pass
            my_book['partner_id'] =  self.pp_url['partner_id']
            book['pp_url'] = self.pp_url[''] % my_book

    def fulfillRequirements(self, book):
        if not self.fulfill:
            return True
        else:
            conditions = {}
            for (key, regex) in self.fulfill.get('search').items():
                conditions[key] = str(bool(re.search(regex, book[key], flags=re.IGNORECASE)))
            condition = self.fulfill['condition']
            for (k, b) in conditions.items():
                condition = condition.replace(k, b)
            return eval(condition) 
            

    def applySingleFilter(self, filter_name, f_params):
        try:
            self.logger.debug('Trying to run filter %s with params %s on files: %s' %
              (filter_name, f_params, self.fetched_files))
            filter = Tools.load_filter(filter_name)(self.logger, f_params)
            self.logger.info('Running filter %s' % filter)
            for file in self.fetched_files:
                filter.run(file)
        except Exception as e:
            self.logger.exception('Exception caught while executing filter %s for connector %s' %
              (filter_name, self.name))
            raise e

    '''
    If you want to set filters and params in connector code manually,
    simply overwrite applyFilters, following way:

    def applyFilters(self):
       your_params = .... #dict of filters params {'filter_name1': {params}, filter_name2: {params}}
       filter_names = ... #comman separated list of filter names 
       (case sensitive, filter name means of course name of a class)
       GenericConnector.applyFilters(self, params = your_params, filters filters_list)
    '''
    def applyFilters(self, params={}, filter_names=None):
        filters = filter_names or self.filters
        if self.filters:
            for _file in self.fetched_files:
                backup = _file + '.backup'
                #TODO: removing backup file should be configurable
                shutil.copy2(_file, backup)

            for filter_name in filters.split(','):
                #our config keys should be lower_case
                f_params = params.get(filter_name, self.filters_config.get(filter_name.lower(), {}))
                self.applySingleFilter(filter_name, f_params)

    def measureLenghtDict(self, dic):
        if self.max_len == {}:
            self.max_len = dict(dic)
            for key in self.max_len.keys():
                if not dic[key]:
                    self.max_len[key] = 0
                    self.max_len_entry[key] = ''
                else:
                    self.max_len[key] = len(dic[key])
                    self.max_len_entry[key] = dic[key]
        else:
            for key in dic.keys():
                try:
                    if dic.get(key) != None and (self.max_len.get(key) == None or self.max_len[key] < len(dic[key])):
                            self.max_len[key] = len(dic[key])
                            self.max_len_entry[key] = dic[key]
                except AttributeError:
                    self.max_len[key] = len(dic[key])
                    self.max_len_entry[key] = dic[key]

    def downloadFile(self, url=None, filename=None, headers={}):
        if not url:
            url = self.url

        req = urllib2.Request(url, headers=headers)

        if self.password and self.username:
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % base64string)

        u = urllib2.urlopen(req)

        if self.backup_dir and not os.path.exists(self.backup_dir):

            os.makedirs(self.backup_dir)

        if filename:
            filename = os.path.join(self.backup_dir, filename)
        else:
            filename = os.path.join(self.backup_dir, self.filename)

        f = open(filename, 'wb')
        meta = u.info()
        if meta.getheader("Content-Length"):
            self.logger.info('%s connector, downloading %s into %s (%s bytes)' %
            (self.name, url, filename, int(meta.getheader('Content-Length'))))
        else:
            self.logger.info('%s connector downloading %s into %s' % (self.name, url, filename))
        if meta.getheader("Last-Modified"):
            self.logger.info('File last modified: %s' % meta.getheader('Last-Modified'))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            self.bookstore_cmd_status.feed_dog()

        f.close()
        self.logger.debug('Download of %s completed, downloaded %d bytes' % (filename, file_size_dl))
        return filename

    def unpackBZIP(self, bz2name):
        return self.unpack_GZIP_BZIP(bz2name, bz2.BZ2File)

    def unpackGZIP(self, gzipname):
        return self.unpack_GZIP_BZIP(gzipname, gzip.GzipFile)

    def unpack_GZIP_BZIP(self, zipname, unpack_fun):
        fh = unpack_fun(zipname, "r")

        file_content = fh.read()
        fh.close()

        if not self.unpack_file:
            self.unpack_file, ext = os.path.splitext(os.path.basename(zipname))
        if self.unpack_dir and not os.path.exists(self.unpack_dir):
                os.makedirs(self.unpack_dir)

        unpack_file_name = os.path.join(self.unpack_dir, self.unpack_file)
        self.fetched_files.append(unpack_file_name)
        self.logger.debug('Unpacking %s into %s' % (zipname, unpack_file_name))
        file = open(unpack_file_name, "w")
        file.write(file_content)
        file.close()
        #result should be a list
        return [unpack_file_name]

    def unpackZIP(self, zipname):
        zfile = zipfile.ZipFile(zipname)
        unpacked_files = []
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            dirname = os.path.join(self.unpack_dir, dirname)
            self.logger.debug('Unpacking zip %s into %s' % (filename, dirname))
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            unpacked_file = os.path.join(dirname, name)
            fd = open(unpacked_file, "w")
            fd.write(zfile.read(name))
            fd.close()
            unpacked_files.append(unpacked_file)
        return unpacked_files

    def save_time_of_(self, column__event_name):
        if self.update_status_service:
            setattr(self.update_status_service, column__event_name, datetime.now())
            self.update_status_service.session.commit()

    def howManyOffers(self):
        Book = GenericBook.getConcretizedClass(context=self)
        return  self.session.query(Book).count()

    def howManyNewOffers(self):
        Book = GenericBook.getConcretizedClass(context=self)
        return  self.session.query(Book).filter(Book.mini_book_id == None).count()

    def howManyOffersParsed(self):
        pass

    def howManyOffersInPromotion(self):
        pass

    def calculateChecksum(self):
        pass

    #FIXME: refactoring, DataStorageWrapper
    def save_info_about_offers(self, offers = None, offers_parsed = None, offers_new = None, offers_promotion = None):
        if self.update_status_service:
            self.update_status_service.offers = offers if offers else self.howManyOffers()
            self.update_status_service.offers_parsed = offers_parsed if offers_parsed else self.howManyOffersParsed()
            self.update_status_service.offers_new = offers_new if offers_new else self.howManyNewOffers()
            self.update_status_service.offers_promotion = offers_promotion if offers_promotion else self.howManyOffersInPromotion()

    # FIXME, TODO: T663 - Aktualizacja się nie wykonuje, jeżeli poprzednim
    # razem był ściągany taki sam plik (checksum), a później nastąpił błąd
    def areDataDifferentThanPrevious(self):
        bcs = self.bookstore_cmd_status

        fetch_command_status = BookstoreCommandStatus.objects.filter(
            type=BookstoreCommandStatus.TYPE_FETCH,
            cmd_status=bcs.cmd_status,
            bookstore_id=bcs.bookstore_id
        ).order_by('id')
        fetch_command_status = list(fetch_command_status)[-1]
        checksum = dict(fetch_command_status.extra).get('checksum', '')

        latest_bcs = BookstoreCommandStatus.objects.filter(
            type=BookstoreCommandStatus.TYPE_FETCH,
            success=True,
            bookstore_id=bcs.bookstore_id
        ).exclude(
            id=fetch_command_status.id
        ).order_by('id')

        if not latest_bcs:
            return True

        latest_bcs = list(latest_bcs)[-1]

        latest_checksum = dict(latest_bcs.extra).get('checksum', '')
        return latest_checksum != checksum

    #TODO: move to SqlWrapper
    @classmethod
    def get_or_create_(cls, session, ClassName, d, param_name=None):
        c = None
        if param_name == None:
            c = session.query(ClassName).filter_by(**d).first()
        elif d.get(param_name) != None:
            c = session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()

        if not c:
            c = ClassName(**d)
        return c

    #TODO: move to SqlWrapper
    @classmethod
    def get_(cls, session, ClassName, d, param_name=None):
        if param_name == None:
            return session.query(ClassName).filter_by(**d).first()
        else:
            return (session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()) if d.get(param_name) != None else None

    def new_add_record(self, d):

        from spistresci.models import MiniBook, Bookstore
        bookstore = Bookstore.objects.get(name=self.name)

        add_MiniBook(bookstore, d)

    def add_record(self, d):
        #TODO: made this thread safe
        if not GenericConnector.rows_initialized:
            PersonRole.init_rows()
            GenericConnector.rows_initialized = True

        Book = GenericBook.getConcretizedClass(context=self)
        Author = GenericAuthor.getConcretizedClass(context=self)
        BooksAuthors = GenericBooksAuthors.getConcretizedClass(context=self)
        ISBN = GenericISBN.getConcretizedClass(context=self)
        Format = GenericFormat.getConcretizedClass(context=self)

        #Session = sessionmaker(bind=SqlWrapper.getEngine())
        session = self.session #Session()
        self.session_obj_counter += 1

        search_keys = [c.name for c in Book.__table__.columns if (c.unique or c.primary_key) and c.name not in ['id', 'mini_book_id', 'description_id']]
        get_dict = {}
        for key in search_keys:
            get_dict[key] = d[key]

        book = self.get_(session, Book, get_dict)

        if not book:
            book = Book(d)
            if d.get('description') != None:
                desc = BookDescription(d)
                book.description = desc

            from models import BookType
            book.book_type = BookType.get_or_create(session, Book.id, d['book_type'])

            if d.get('isbns') != None:
                for isbn_d in d['isbns']:
                    #if self.get_(session, ISBN, isbn_d, 'raw',) != None:
                    #    isbn = ISBN.get_or_create(session, isbn_d, 'raw')
                    #else:
                    #    isbn = ISBN.get_or_create(session, isbn_d, 'core')
                    isbn = ISBN(**isbn_d)
                    book.isbns.append(isbn)

            if d.get('formats') != None:
                for format in d['formats']:
                    f = Format.get_or_create(session, Book.id, format, {"name":format})
                    book.formats.append(f)

            if d.get('persons') != None:
                for role_dict in d['persons']:
                    role = role_dict.keys()[0]
                    list_of_person_dicts = role_dict[role]

                    role_ = PersonRole.get_or_create(session, Book.id, role, {"name":role})
                    for person_dict in list_of_person_dicts:
                        author = Author.get_or_create(session, person_dict)
                        books_authors = BooksAuthors()
                        books_authors.role = role_
                        books_authors.book = book
                        books_authors.author = author
                        session.add(books_authors)

            book.update_timestamp = book.update_minidata_timestamp = self.update_status_service.timestamp
            session.add(book)
        else:
            book.update(d, session, self)

        if self.session_obj_counter == self.session_obj_limit:
            session.commit()
            self.session_obj_counter = 0

        #session.close()


# class GenericBook(GenericBase):
#     id = Column(Integer, primary_key=True)
#     external_id = Column(Integer, unique=True)
#     title = Column(Unicode(256))
#     price = Column(Integer) #price in grosz
#     #if price_normal == -1 it means there is no special offer for this book
#     price_normal = Column(Integer, default=-1) #price in grosz
#     #status = Column(Integer)
#     url = Column(STUrl)
#     pp_url = Column(STUrl)
#     cover = Column(STUrl)
#
#     @declared_attr
#     def book_type_id(cls):
#         return Column(Integer, ForeignKey('BookType.id'))
#
#     @declared_attr
#     def book_type(cls):
#         return relationship("BookType")
#
#     @declared_attr
#     def declareTablesFor(cls):
#         connector_name = cls.__tablename__[:-len("Book")]
#         for table_name in ["Author", "BookPrice", "BooksAuthors", "ISBN", "BooksFormats", "Format"]:
#             t = 'class %s%s(%s%s, Base): pass' % (connector_name, table_name, "Generic", table_name)
# #            print t
#             exec(t)
#
#     @declared_attr
#     def description_id(cls):
#         return Column(Integer, ForeignKey('BookDescription.id'), unique=True)
#
#     @declared_attr
#     def description(cls):
#         return relationship("BookDescription", uselist=False)
#
#     @declared_attr
#     def isbns(cls):
#         return relationship(cls.__tablename__[:-len("Book")] + "ISBN", backref="book", lazy='dynamic')
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     @declared_attr
#     def mini_book_id(cls):
#         return Column(Integer, ForeignKey('MiniBook.id'), unique=True)
#
#     @declared_attr
#     def mini_book(cls):
#         return relationship("MiniBook", uselist=False)
#
#     update_timestamp = Column(Integer)
#     update_minidata_timestamp = Column(Integer)
#
#
# #TODO: how to do this?
# #    '''this is title presented to frontend'''
# #    @declared_attr
# #    def org_title(cls):
# #        return cls.title
#
#     @declared_attr
#     def authors(cls):
#         name = cls.__tablename__[:-len("Book")]
#         return association_proxy(name + "_authorship", "author")
#
#     def __init__(self, initial_data):
#         for key in initial_data:
#             try:
#                 if getattr(self, key) == None:
#                     setattr(self, key, initial_data[key])
#             except AttributeError:
#                 pass
#
#     #DoNotLetCommit
#     def update(self, new_data, session, connector):
#         for key in new_data:
#             try:
#                 un = unicode(getattr(self, key))
#
#                 updated_minidata = False
#                 updated = False
#
#                 if key == 'persons':
#                     updated_minidata |= self.update_relation(session, new_data, "authors", GenericAuthor.getConcretizedClass(context=self))
#                 elif key == 'isbns':
#                     updated_minidata |= self.update_relation(session, new_data, "isbns", GenericISBN.getConcretizedClass(context=self))
#                 elif key == 'formats':
#                     updated_minidata |= self.update_relation(session, new_data, "formats", GenericFormat.getConcretizedClass(context=self))
#                 elif key == 'description':
#                     if self.description.description != new_data[key]:
#                         self.description.description = new_data[key]
#                         updated = True
#                 elif key == 'price':
#                     #special case of updating price is handle by trigger
#                     if un != new_data[key]:
#                         setattr(self, key, new_data[key])
#                         updated_minidata |= True
#
#                 elif un != new_data[key]:
#                     setattr(self, key, new_data[key])
#                     from final import MiniBook
#                     #This is a hack
#                     #There is no pp_url in MiniBook table however if pp_url is changed, minibook should be updated
#                     updated_minidata |= (key in MiniBook.__table__.columns._data.keys() or key == 'pp_url')
#
#                 if updated_minidata:
#                     self.update_minidata_timestamp = connector.update_status_service.timestamp
#                     self.update_timestamp = connector.update_status_service.timestamp
#                 elif updated:
#                     self.update_timestamp = connector.update_status_service.timestamp
#
#             except AttributeError:
#                 pass
#
#     def update_relation(self, session, new_data, foos, Foo):
#         updated = False
#         str_foos = []
#         self_foos = getattr(self, foos)
#
#         for foo in self_foos:
#             str_foos.append(unicode(foo))
#
#         if sorted(str_foos) != sorted(new_data[foos]):
#
#             for foo in new_data[foos]:
#                 if foo not in str_foos:
#                     f = Foo.get_or_create(session, foo)
#                     self_foos.append(f)
#                     session.add(f)
#                     updated = True
#
#             for foo in str_foos:
#                 if foo not in new_data[foos]:
#                     f = Foo.get_or_create(session, foo)
#                     self_foos.remove(f)
#                     updated = True
#
#         return updated
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'Book')
#
# class GenericAuthor(GenericBase):
#     id = Column(Integer, primary_key=True)
#     name = Column(Unicode(255))#, unique=True)
#     firstName = Column(Unicode(32))
#     middleName = Column(Unicode(32))
#     lastName = Column(Unicode(32))
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     @declared_attr
#     def books(cls):
#         name = cls.__tablename__[:-len("Author")]
#         return association_proxy(name + "_authorship", "book")
#
#     def __unicode__(self):
#         return unicode(self.name)
#
#     @classmethod
#     def get_or_create(cls, session, author):
#         return GenericConnector.get_or_create_(session, cls, author, 'name')
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'Author')
#
# class GenericBookPrice(GenericBase):
#
#     id = Column(Integer, primary_key=True)
#     @declared_attr
#     def book_id(cls):
#         return Column(Integer, ForeignKey(cls.__tablename__[:-len("Price")] + '.id'))
#
#     price = Column(Integer)
#     date = Column(DateTime)
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
# class GenericBooksAuthors(GenericBase):
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     id = Column(Integer, primary_key=True)
#
#     @declared_attr
#     def role_name(cls):
#         return Column(Unicode(15), ForeignKey('PersonRole.name'))
#
#     @declared_attr
#     def role(cls):
#         return relationship("PersonRole", uselist=False)
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'BooksAuthors')
#
#     @declared_attr
#     def book_id(cls):
#         name = cls.__tablename__[:-len("BooksAuthors")]
#         return Column(Integer, ForeignKey(name + 'Book.id'))
#
#     @declared_attr
#     def author_id(cls):
#         name = cls.__tablename__[:-len("BooksAuthors")]
#         return Column(Integer, ForeignKey(name + 'Author.id'))
#
#     @declared_attr
#     def book(cls):
#         name = cls.__tablename__[:-len("BooksAuthors")]
#         table = cls.registered[name + 'Book']
#         return relationship(table, backref=name + "_authorship")
#
#     @declared_attr
#     def author(cls):
#         name = cls.__tablename__[:-len("BooksAuthors")]
#         table = cls.registered[name + 'Author']
#         return relationship(table, backref=name + "_authorship")
#
# class GenericISBN(GenericBase):
#     id = Column(Integer, primary_key=True)
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     @declared_attr
#     def book_id(cls):
#         return Column(Integer, ForeignKey(cls.__tablename__[:-len("ISBN")] + 'Book.id'))
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'ISBN')
#
#     @classmethod
#     def get_or_create(cls, session, isbn_dict, param_name):
#         return GenericConnector.get_or_create_(session, cls, isbn_dict, param_name)
#
#     raw = Column(Unicode(50))
#     core = Column(Unicode(9))
#     isbn10 = Column(Unicode(10))
#     isbn13 = Column(Unicode(13))
#     valid = Column(Boolean)
#
# class GenericBooksFormats(GenericBase):
#     id = Column(Integer, primary_key=True)
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'BooksFormats')
#
#     @declared_attr
#     def book_id(cls):
#         name = cls.__tablename__[:-len("BooksFormats")]
#         return Column(Integer, ForeignKey(name + 'Book.id'))
#
#     @declared_attr
#     def format_id(cls):
#         name = cls.__tablename__[:-len("BooksFormats")]
#         return Column(Integer, ForeignKey(name + 'Format.id'))
#
# class GenericFormat(GetOrCreateCache, GenericBase):
#     id = Column(Integer, primary_key=True)
#     name = Column(Unicode(10))
#
#     @declared_attr
#     def __tablename__(cls):
#         cls.register()
#         return cls.__name__
#
#     @declared_attr
#     def books(cls):
#         name = cls.__tablename__[:-len("Format")]
#         return relationship(name + "Book", secondary = cls.metadata.tables[name + 'BooksFormats'] , backref = backref("formats", lazy = 'joined'), lazy = 'joined')
#
#     @staticmethod
#     def getConcretizedClass(context):
#         return GenericBase.getConcretizedClass(context, 'Format')
