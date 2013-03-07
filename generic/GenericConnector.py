import urllib2
import zipfile
import tarfile
import gzip
import tarfile
import os.path
import shutil
from datetime import datetime

import ConfigParser
from connectors_logger import logger_instance
import utils
#interesting thing: utils.Enum is hide by sql_wrapper.Enum 
from sql_wrapper import *
from pyisbn import *

registered={}

class GenericBase(object):
    @staticmethod
    def getConcretizedClass(context, className):
        if "Author" in context.name:
            return registered[context.name[:-len("Author")] + className]
        elif "Book" in context.name:
            return registered[context.name[:-len("Book")] + className]
        elif "BookDescription" in context.name:
            return registered[context.name[:-len("BookDescription")] + className]
        else: #Connector
            return registered[context.name + className]


class GenericConnector(object):
   
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
        cls.config_object = ConfigParser.ConfigParser()
        if not cls.config_object.read(cls.config_file):
            raise ConfigParser.Error('Could not read config from file %s'%cls.config_file)

    @classmethod
    def class_name(cls):
        return cls.__name__

    @property
    def name(self):
        return self._name

    
    def _parse_config(self, config_file='conf/connectors.ini', section=None, config_object = None):
        if not config_object:
            self.read_config()
        else:
             self.config_object = config_object
        if not section:
           section = self.name
        self.section = section

        self.config = dict(self.config_object.items(self.section,
                        vars={'date':datetime.now().strftime('%Y%m%d%H%M%S')}
                      ))
        
    def __init__(self, name=None):
        if not name:
            self._name = self.class_name()
        else:
            self._name = name
        self.register()
        self._parse_config(self.config_file, config_object=self.config_object)
        self.url = self.config['url']
        self.filename = self.config['filename']
        self.backup_dir = self.config.get('backup_dir', '')
        print self.ArchiveType.NONE
        self.backup_archive = self.ArchiveType.int(self.config.get('backup_archive','NONE'))
        self.unpack_file = self.config.get('unpack_file', '')
        self.unpack_dir = self.config.get('unpack_dir', '')
        self.archive_file = self.config.get('archive_file','')
        self.remove_unpacked = int(self.config.get('remove_unpacked', 1))
        self.log_config=self.config.get('log_config', 'conf/log.connectors.ini')
        self.logger = logger_instance(self.log_config)
        self.log_erratum_config=self.config.get('log_erratum_config', 'conf/log.erratum.ini')
        self.erratum_logger = logger_instance(self.log_erratum_config)
        self.logger.debug('%s connector created'%self.name)
        self.mode = self.BookList_Mode.int(self.config.get('mode','UNKNOWN'))
  

    def register(self):
        registered[self.name]=type(self)
   

    def __del__(self):
        self.logger.debug('Cleaning up after executing %s connector'%self.name)
        if self.backup_dir:
            if self.backup_archive in [self.ArchiveType.BZIP, self.ArchiveType.GZ] and \
               self.mode not in [self.BookList_Mode.ZIPPED_XMLS, self.BookList_Mode.GZIPPED_XMLS]:
                self.compress_dir(self.backup_dir, self.backup_archive)
                self.backup_archive = self.ArchiveType.NONE
                 
            if self.backup_archive == self.ArchiveType.NONE and os.path.exists(self.backup_dir):
                self._rm_ifpossible(self.backup_dir, 'backup')
                self.backup_dir=''

        if self.unpack_dir and self.remove_unpacked and os.path.exists(self.unpack_dir):
            self._rm_ifpossible(self.unpack_dir, 'unpack')
            self.unpack_dir=''

    def _rm_ifpossible(self, path, dir_type='backup'):
        cwd = os.getcwd().rstrip('/')+'/'
        abs_path = os.path.abspath(path).rstrip('/')+'/'
        if abs_path in cwd:
            raise IOError(
            'Are you insane or something?. Don\'t tell me to remove whole my working dir (%s). HINT:%s dir should not be current dir or parent'%(path, dir_type)
            )
        self.logger.debug('Connector %s. Removing %s dir %s'%(self.name, dir_type, path))
        shutil.rmtree(path)


    def compress_dir(self, path, archive_type):
        if archive_type == self.ArchiveType.GZ:
            mode = 'gz'
        else:
            mode = 'bz2'
        path = os.path.abspath(path)
        basename = os.path.basename(path)
        tar_name = os.path.abspath(os.path.join(path, '..' ,'%s.tar.%s'%(basename, mode)))
        self.logger.debug('Comprassing dir %s to %s', path, tar_name)
        tar = tarfile.open(tar_name, 'w:%s'%mode)
        tar.add(path, arcname = basename)     


    #@abc.abstractmethod    
    def fetchData(self):
        """parse fetchData"""
    
    #@abc.abstractmethod    
    def parse(self):
        """parse method"""

    #@abc.abstractmethod        
    def updateDatabase(self):
        """update method"""

    def mesureLenght(self, list):
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

    def mesureLenghtDict(self, dic):
        if self.max_len == {}:
            self.max_len = dict(dic)
            for key in self.max_len.keys():
                if not dic[key]:
                    self.max_len[key] = 0
                    self.max_len_entry[key]=''
                else:
                    self.max_len[key]=len(dic[key])
                    self.max_len_entry[key]=dic[key]
        else:
            for key in dic.keys():
                try:
                    if dic[key] != None and self.max_len[key] < len(dic[key]):
                        self.max_len[key] = len(dic[key])
                        self.max_len_entry[key] = dic[key]
                except AttributeError:
                    self.max_len[key] = len(dic[key])
                    self.max_len_entry[key] = dic[key]

    def validate(self, dic):
        id=dic.get('external_id')
        title=dic.get('title')
        self.validateISBN(dic, id, title)
        self.validatePrice(dic, id, title)
        self.validateSize(dic, id, title)

    def validateISBN(self, dic, id, title):
        original_isbn = dic.get('isbn')
        isbn_str=""

        if original_isbn != None:
            try:
                isbn = Isbn(original_isbn)
                if isbn.validate():
                    isbn_str = isbn.isbn
                else:
                    self.erratum_logger.info("ISBN validation failed! connector: %s, original_isbn: %s, cannonical ISBN: %s, id: %s, title: %s"%(self.name[:-len("Book")], original_isbn, isbn.isbn, id, title))

            except IsbnError:
                if original_isbn == '':
                    self.erratum_logger.warning("Entry does not have ISBN! connector: %s, id: %s, title: %s"%(self.name, id, title))
                else:
                    self.erratum_logger.info("ISBN has wrong format! connector: %s, original_isbn: %s, id: %s, title: %s"%(self.name[:-len("Book")], original_isbn, id, title))

        dic['isbn']=isbn_str

    def validatePrice(self, dic, id, title):
        original_price = dic.get('price')
        price=0
        if original_price != None:
            price_str=original_price
            if "," in price_str:
                price_str = price_str.replace(",", ".")

            if "." in price_str:
                if price_str.count(".")==1:
                    price_str = price_str.replace(".", "")
                else:
                    self.erratum_logger.warning("Entry has price in wrong format! connector: %s, id: %s, title: %s"%(self.name, id, title))

            try:
                price = int(price_str)
            except ValueError:
                self.erratum_logger.warning("Entry has price in wrong format! connector: %s, id: %s, title: %s"%(self.name, id, title))

        dic['price']=unicode(price)


    def validateSize(self, dic, id, title):
        pass


    def downloadFile(self, url=None, filename=None, headers = None):
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
            self.logger.info('%s connector downloading %s into %s'%(self.name, url, filename))
        if meta.getheader("Last-Modified"):
            self.logger.info('File last modified: %s'%meta.getheader('Last-Modified'))
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)

        f.close()
        self.logger.debug('Download of %s completed, downloaded %d bytes'%(filename,file_size_dl))
        return filename

    def unpackGZIP(self, gzipname):
        fh = gzip.GzipFile(gzipname, "r")
        
        file_content = fh.read()
        fh.close()

        if not self.unpack_file:
            self.unpack_file, ext = os.path.splitext(os.path.basename(gzipname))
        if self.unpack_dir and not os.path.exists(self.unpack_dir):
                os.makedirs(self.unpack_dir)
     
        unpack_file_name =  os.path.join(self.unpack_dir,self.unpack_file)
        self.logger.debug('Unpacking gzip %s into %s'%(gzipname,unpack_file_name))
        file = open(unpack_file_name, "w")
        file.write(file_content)
        file.close()
        
    def unpackZIP(self, zipname):
        zfile = zipfile.ZipFile(zipname)
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
            dirname = os.path.join(self.unpack_dir,dirname)
            self.logger.debug('Unpacking zip %s into %s'%(filename,dirname))
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            fd = open(os.path.join(dirname,name),"w")
            fd.write(zfile.read(name))
            fd.close()

    @classmethod
    def get_or_create_(cls, ClassName, param_name, d, session):
        c = session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()
        if not c:
            c = ClassName(**d)
        return c
    
    def get_(self, ClassName, param_name, d, session):
        return session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()

       
    def add_record(self, d):
        Book =  GenericBook.getConcretizedClass(context=self)
        Description = GenericBookDescription.getConcretizedClass(context=self)
        Author = GenericAuthor.getConcretizedClass(context=self)
        
        Session = sessionmaker(bind=SqlWrapper.getEngine())
        session = Session()
        
        book = self.get_(Book, "external_id", d, session)

        if not book:
            book=Book(d)
            if d.get('description') != None:
                desc=Description(d)
                book.description=desc

            for author in d['authors']:
                a = Author.get_or_create(author, session)
                a.books.append(book)
                session.add(a)
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

    @declared_attr
    def description(cls):
        return relationship(cls.__tablename__+"Description", uselist=False, backref="book")

    @declared_attr
    def __tablename__(cls):
        registered[cls.__name__]=cls
        return cls.__name__

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
                    str_author_list=[]
                    for author in self.authors:
                        str_author_list.append(unicode(author))

                    if sorted(str_author_list) != sorted(new_data['authors']):
                        Author = GenericAuthor.getConcretizedClass(context=self)

                        for str_author in new_data['authors']:
                            if str_author not in str_author_list:
                                a = Author.get_or_create(str_author, session)
                                #a.books.append(self)
                                self.authors.append(a)
                                session.add(a)

                        for str_author in str_author_list:
                            if str_author not in new_data['authors']:
                                a = Author.get_or_create(str_author, session)
                                self.authors.remove(a)
                                session.commit()

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
        registered[cls.__name__]=cls
        return cls.__name__

    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Description")]+'.id'))

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
    name = Column(Unicode(255), unique=True)

    @declared_attr
    def __tablename__(cls):
        registered[cls.__name__]=cls
        return cls.__name__

    @declared_attr
    def books(cls):
        name = cls.__tablename__[:-len("Author")]
        return relationship(name+'Book', secondary=Table(name+'_books_authors',
                                      SqlWrapper.getBaseClass().metadata,
                                      Column('book_id', Integer, ForeignKey(name+'Book.id')),
                                      Column('author_id', Integer, ForeignKey(name+'Author.id'))
                                      ), backref='authors')
    def __unicode__(self):
        return unicode(self.name)

    @classmethod
    def get_or_create(cls, author, session):
        return GenericConnector.get_or_create_(cls, 'name', {'name':author}, session)

    @staticmethod
    def getConcretizedClass(context):
        return GenericBase.getConcretizedClass(context, 'Author')

class GenericBookPrice(GenericBase):

    id = Column(Integer, primary_key=True)
    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Price")]+'.id'))

    price = Column(Integer)
    date = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        registered[cls.__name__]=cls
        return cls.__name__
