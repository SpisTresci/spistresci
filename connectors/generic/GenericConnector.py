import urllib2
import zipfile
import tarfile
import gzip
import os.path
import shutil
from datetime import datetime

import ConfigParser
from utils import logger_instance
from utils import DataValidator
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import class_mapper
import utils
#interesting thing: utils.Enum is hide by sql_wrapper.Enum
from sqlwrapper import *
from connectors import Tools

Base = SqlWrapper.getBaseClass()

class InvalidContext(Exception):
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
        if context.name.endswith('Author'):
            return GenericBase.registered[context.name[:-len('Author')] + className]
        elif context.name.endswith('Book'):
            return GenericBase.registered[context.name[:-len('Book')] + className]
        elif context.name.endswith('BookDescription'):
            return GenericBase.registered[context.name[:-len('BookDescription')] + className]
        elif context.name.endswith('BooksAuthors'):
            return GenericBase.registered[context.name[:-len('BooksAuthors')] + className]
        elif context.name.endswith('ISBN'):
            return GenericBase.registered[context.name[:-len('ISBN')] + className]
        elif context.name.endswith('Format'):
            return GenericBase.registered[context.name[:-len('Format')] + className]
        else: #Connector
            return GenericBase.registered[context.name + className]

class GenericConnector(GenericBase, DataValidator):

    '''
    NONE - remove backup dir after execution
    UNCOMPRESSED - do not touch backup dir after execution
    BZIP - create tar.bz2 archive
    GZIP - create tar.gz archive
    '''
    class ArchiveType(utils.Enum):
        values = ['NONE', 'UNCOMPRESSED', 'BZIP', 'GZ']

    class BookList_Mode(utils.Enum):
        values = [
            'UNKNOWN',
            'SINGLE_XML',
            'ZIPPED_XMLS',
            'GZIPPED_XMLS',
            'MULTIPLE_XMLS',
        ]

    max_len = {}
    max_len_entry = {}

    config_file = 'conf/connectors.ini'
    config_object = None

    @classmethod
    def read_config(cls):
        cls.config_object = ConfigParser.SafeConfigParser()
        #TODO: our config should be case sensitive, somehow this does not work
        #cls.config_object.optionxfrom = str
        if not cls.config_object.read(cls.config_file):
            raise ConfigParser.Error('Could not read config from file %s' % cls.config_file)

    @classmethod
    def class_name(cls):
        return cls.__name__

    @property
    def name(self):
        return self._name

    def _get_conf_option(self, _list, value, dic):
        key = _list[0]
        _list = _list[1:]
        old_value = {}
        if type(dic) is dict:
            old_value = dic.get(key, {})
        if not type(old_value) is dict:
            old_value = {'':old_value}
        if _list:
            old_value[_list[0]] = self._get_conf_option(_list, value, old_value)
        else:
            old_value[''] = value
        if old_value.keys() == ['']:
            old_value = old_value['']
        return old_value


    def parse_config(self, config_file='conf/connectors.ini', section=None, config_object=None):
        if not config_object:
            self.read_config()
        else:
             self.config_object = config_object
        if not section:
           section = self.name
        self.section = section
        self.config = {}
        for item in self.config_object.items(self.section,
                        vars={'date':datetime.now().strftime('%Y%m%d%H%M%S'),
                              'connector_lowcase':self.name.lower(),
                              'connector':self.name}):

            #this is for managaging config options like
            #option.suboption = 11
            (key, value) = item
            splited = key.split('.')
            self.config[splited[0]] = self._get_conf_option(splited, value, self.config)

    def __init__(self, name=None):
        if not name:
            self._name = self.class_name()
        else:
            self._name = name
        self.register()
        self.parse_config(self.config_file)
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
        self.log_config = self.config.get('log_config', 'conf/log.connectors.ini')
        self.logger = logger_instance(self.log_config)
        self.log_erratum_config = self.config.get('log_erratum_config', 'conf/log.erratum.ini')
        self.erratum_logger = logger_instance(self.log_erratum_config)
        self.logger.debug('%s connector created' % self.name)
        self.mode = self.BookList_Mode.int(self.config.get('mode', 'UNKNOWN'))
        self.filters_config = self.config.get('filters', {})
        if type(self.filters_config) is dict:
            self.filters = self.filters_config.get('')
        else:
            self.filters = self.filters_config
            self.filters_config = {}
        self.fetched_files = []
        self.loadListOfNames()

    def __del__(self):
        self.logger.debug('Cleaning up after executing %s connector' % self.name)
        if self.backup_dir:
            if self.backup_archive in [self.ArchiveType.BZIP, self.ArchiveType.GZ] and \
               self.mode not in [self.BookList_Mode.ZIPPED_XMLS, self.BookList_Mode.GZIPPED_XMLS]:
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


    #@abc.abstractmethod
    def fetchData(self):
        """fetchData method"""
        pass

    #@abc.abstractmethod
    def parse(self):
        """parse method"""
        pass

    #@abc.abstractmethod
    def updateDatabase(self):
        """update method"""
        pass

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

    def measureLenght(self, list):
        if self.max_len == []:
            for i in range(len(list)):
                if not list[i]:
                    self.max_len.append(0)
                    self.max_len_entry.append('')
                else:
                    self.max_len.append(len(list[i]))
                    self.max_len_entry.append(list[i])
        else:
            for i in range(len(list)):
                if list[i] != None and self.max_len[i] < len(list[i]):
                    self.max_len[i] = len(list[i])
                    self.max_len_entry[i] = list[i]

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

    def downloadFile(self, url=None, filename=None, headers=None):
        if not url:
            url = self.url
        if headers:
            req = urllib2.Request(url, headers=headers)
            u = urllib2.urlopen(req)
        else:
            u = urllib2.urlopen(url)
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

        f.close()
        self.logger.debug('Download of %s completed, downloaded %d bytes' % (filename, file_size_dl))
        return filename

    def unpackGZIP(self, gzipname):
        fh = gzip.GzipFile(gzipname, "r")

        file_content = fh.read()
        fh.close()

        if not self.unpack_file:
            self.unpack_file, ext = os.path.splitext(os.path.basename(gzipname))
        if self.unpack_dir and not os.path.exists(self.unpack_dir):
                os.makedirs(self.unpack_dir)

        unpack_file_name = os.path.join(self.unpack_dir, self.unpack_file)
        self.fetched_files.append(unpack_file_name)
        self.logger.debug('Unpacking gzip %s into %s' % (gzipname, unpack_file_name))
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

    def get_(self, session, ClassName, d, param_name=None):
        if param_name == None:
            return session.query(ClassName).filter_by(**d).first()
        else:
            return (session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()) if d.get(param_name) != None else None

    def add_record(self, d):
        Book = GenericBook.getConcretizedClass(context=self)
        Description = GenericBookDescription.getConcretizedClass(context=self)
        Author = GenericAuthor.getConcretizedClass(context=self)
        BooksAuthors = GenericBooksAuthors.getConcretizedClass(context=self)
        ISBN = GenericISBN.getConcretizedClass(context=self)
        Format = GenericFormat.getConcretizedClass(context=self)

        Session = sessionmaker(bind=SqlWrapper.getEngine())
        session = Session()

        search_keys = [c.name for c in Book.__table__.columns if c.unique or c.primary_key]
        search_keys.remove('id')
        get_dict = {}
        for key in search_keys:
            get_dict[key] = d[key]

        book = self.get_(session, Book, get_dict)

        if not book:
            book = Book(d)
            if d.get('description') != None:
                desc = Description(d)
                book.description = desc

            if d.get('isbns') != None:
                for isbn_d in d['isbns']:
                    if self.get_(session, ISBN, isbn_d, 'raw',) != None:
                        isbn = ISBN.get_or_create(session, isbn_d, 'raw')
                    else:
                        isbn = ISBN.get_or_create(session, isbn_d, 'core')

                    book.isbns.append(isbn)

            if d.get('formats') != None:
                for format in d['formats']:
                    f = Format.get_or_create(session, format)
                    book.formats.append(f)

            for touple in [('authors', False, False), ('translators', True, False), ('lectors', False, True)]:
                if d.get(touple[0]) != None:
                    for author in d[touple[0]]:
                        author = Author.get_or_create(session, author)
                        books_authors = BooksAuthors(is_translator=touple[1], is_lector=touple[2])
                        books_authors.book = book
                        books_authors.author = author
                        session.add(books_authors)

            session.add(book)
            session.commit()
        else:
            book.update(d, session)
            session.commit()

        session.close()

class GenericBook(GenericBase):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255))
    external_id = Column(Integer, unique=True)
    price = Column(Integer)                     #GROSZE!!!

    @declared_attr
    def declareTablesFor(cls):
        connector_name = cls.__tablename__[:-len("Book")]
        for table_name in ["BookDescription", "Author", "BookPrice", "BooksAuthors", "BooksISBNs", "ISBN", "BooksFormats", "Format"]:
            t = 'class %s%s(%s%s, Base): pass' % (connector_name, table_name, "Generic", table_name)
#            print t
            exec(t)

    @declared_attr
    def description(cls):
        return relationship(cls.__tablename__ + "Description", uselist=False, backref="book")

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @declared_attr
    def authors(cls):
        name = cls.__tablename__[:-len("Book")]
        return association_proxy(name + "_authorship", "author")

    def __init__(self, initial_data):
        for key in initial_data:
            try:
                if getattr(self, key) == None:
                    setattr(self, key, initial_data[key])
            except AttributeError:
                pass

    def update(self, new_data, session):
        new_book = type(self)(new_data)
        for key in new_data:
            try:
                atr_type = type(getattr(self, key))
                un = unicode(getattr(self, key))

                if key == 'authors':
                    str_author_list = []
                    for author in self.authors:
                        str_author_list.append(unicode(author))

                    if sorted(str_author_list) != sorted(new_data['authors']):
                        Author = GenericAuthor.getConcretizedClass(context=self)

                        for str_author in new_data['authors']:
                            if str_author not in str_author_list:
                                a = Author.get_or_create(session, str_author)
                                #a.books.append(self)
                                self.authors.append(a)
                                session.add(a)

                        for str_author in str_author_list:
                            if str_author not in new_data['authors']:
                                a = Author.get_or_create(session, str_author)
                                self.authors.remove(a)
                                session.commit()

                elif key == 'isbns':
                    pass
                elif un != new_data[key]:
                    setattr(self, key, new_data[key])

            except AttributeError:
                pass

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'Book')

    
class GenericBookDescription(GenericBase):
    id = Column(Integer, primary_key=True)
    description = Column(Unicode(20000)) #TODO: parametr musi byc dynamicznie ustawiany

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Description")] + '.id'))

    def __init__(self, initial_data):
        try:
            self.description = initial_data['description']
        except:
            exit('Record ' + initial_data + ' doesn\'t have defined desription')

    def __unicode__(self):
        return unicode(self.description)

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'BookDescription')

class GenericAuthor(GenericBase):
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))#, unique=True)
    firstName = Column(Unicode(32))
    middleName = Column(Unicode(32))
    lastName = Column(Unicode(32))


    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @declared_attr
    def books(cls):
        name = cls.__tablename__[:-len("Author")]
        return association_proxy(name + "_authorship", "book")

    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def get_or_create(cls, session, author):
        return GenericConnector.get_or_create_(session, cls, author, 'name')

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'Author')

class GenericBookPrice(GenericBase):

    id = Column(Integer, primary_key=True)
    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Price")] + '.id'))

    price = Column(Integer)
    date = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

class GenericBooksAuthors(GenericBase):

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    id = Column(Integer, primary_key=True)
    is_translator = Column(Boolean)
    is_lector = Column(Boolean)

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'BooksAuthors')

    @declared_attr
    def book_id(cls):
        name = cls.__tablename__[:-len("BooksAuthors")]
        return Column(Integer, ForeignKey(name + 'Book.id'))

    @declared_attr
    def author_id(cls):
        name = cls.__tablename__[:-len("BooksAuthors")]
        return Column(Integer, ForeignKey(name + 'Author.id'))

    @declared_attr
    def book(cls):
        name = cls.__tablename__[:-len("BooksAuthors")]
        table = cls.registered[name + 'Book']
        return relationship(table, backref=name + "_authorship")

    @declared_attr
    def author(cls):
        name = cls.__tablename__[:-len("BooksAuthors")]
        table = cls.registered[name + 'Author']
        return relationship(table, backref=name + "_authorship")


class GenericBooksISBNs(GenericBase):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'BooksISBNs')

    @declared_attr
    def book_id(cls):
        name = cls.__tablename__[:-len("BooksISBNs")]
        return Column(Integer, ForeignKey(name + 'Book.id'))

    @declared_attr
    def isbn_id(cls):
        name = cls.__tablename__[:-len("BooksISBNs")]
        return Column(Integer, ForeignKey(name + 'ISBN.id'))

class GenericISBN(GenericBase):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @declared_attr
    def books(cls):
        name = cls.__tablename__[:-len("ISBN")]
        return relationship(name + "Book", secondary=cls.metadata.tables[name + 'BooksISBNs'] , backref="isbns")

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'ISBN')

    @classmethod
    def get_or_create(cls, session, isbn_dict, param_name):
        return GenericConnector.get_or_create_(session, cls, isbn_dict, param_name)

    raw = Column(Unicode(50), unique=True)
    core = Column(Unicode(9))
    isbn10 = Column(Unicode(10), unique=True)
    isbn13 = Column(Unicode(13), unique=True)
    valid = Column(Boolean)

class GenericBooksFormats(GenericBase):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'BooksFormats')

    @declared_attr
    def book_id(cls):
        name = cls.__tablename__[:-len("BooksFormats")]
        return Column(Integer, ForeignKey(name + 'Book.id'))

    @declared_attr
    def format_id(cls):
        name = cls.__tablename__[:-len("BooksFormats")]
        return Column(Integer, ForeignKey(name + 'Format.id'))

class GenericFormat(GenericBase):
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10))
    @declared_attr
    def __tablename__(cls):
        cls.register()
        return cls.__name__

    @declared_attr
    def books(cls):
        name = cls.__tablename__[:-len("Format")]
        return relationship(name + "Book", secondary=cls.metadata.tables[name + 'BooksFormats'] , backref="formats")

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'Format')

    @classmethod
    def get_or_create(cls, session, format):
        return GenericConnector.get_or_create_(session, cls, {"name":format}, "name")
