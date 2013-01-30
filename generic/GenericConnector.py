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
from utils import Enum

registered={}

class GenericConnector(object):
   
    '''
    NONE - remove backup dir after execution
    UNCOMPRESSED - do not touch backup dir after execution
    BZIP - create tar.bz2 archive
    GZIP - create tar.gz archive
    '''
    class ArchiveType(Enum):
        values = ['NONE', 'UNCOMPRESSED', 'BZIP', 'GZ']

    class BookList_Mode(Enum):
        values = [
            'UNKNOWN',
            'SINGLE_XML',
            'ZIPPED_XMLS',
            'GZIPPED_XMLS',
            'MULTIPLE_XMLS',
        ]

    max_len = []
    max_len_entry = []

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
        
    def __init__(self,name=None):
        self.register()
        if not name:
            self._name = self.class_name()
        else:
            self._name = name
        self._parse_config(self.config_file, config_object=self.config_object)
        self.url = self.config['url']
        self.filename = self.config['filename']
        self.backup_dir = self.config.get('backup_dir', '')
        self.backup_archive = self.ArchiveType.int(self.config.get('backup_archive','NONE'))
        self.unpack_file = self.config.get('unpack_file', '')
        self.unpack_dir = self.config.get('unpack_dir', '')
        self.archive_file = self.config.get('archive_file','')
        self.remove_unpacked = int(self.config.get('remove_unpacked', 1))
        self.log_config=self.config.get('log_config', 'conf/log.connectors.ini')
        self.logger = logger_instance(self.log_config)
        self.logger.debug('%s connector created'%self.name)
        self.mode = self.BookList_Mode.int(self.config.get('mode','UNKNOWN'))
  

    def register(self):
        registered[self.my_name()]=type(self)
   

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

    def downloadFile(self, url=None, filename=None):
        if not url:
            url = self.url
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
            self.unpack_file, ext = os.path.splitext(gzipname)
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

    def get_or_create_(self, ClassName, d, session):
        c = session.query(ClassName).filter_by(**d).first()
        if not c:
            c = ClassName(**d)
        return c
    
    def get_(self, ClassName, param_name, d, session):
        return session.query(ClassName).filter_by(**{param_name:d[param_name]}).first()

       
    def add_record(self, d):
        
        Book = registered[self.name + 'Book']
        Description = registered[self.name + 'BookDescription']
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        book = self.get_(Book, "external_id", d, session)
        if not book:
            book=Book(d)
            desc=Description(d)
            book.description=desc
            session.merge(book)
            session.commit()       
       
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.ext.declarative import declared_attr
Base = declarative_base()
engine  = create_engine('mysql://root:Z0oBvgF1R3@localhost/st', echo=True)

        

class GenericBook(object):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255))
    @declared_attr
    def description(cls):
        return relationship(cls.__tablename__+"Description", uselist=False, backref="book")
    external_id = Column(Integer, unique=True)
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

    
    #@declared_attr
    #def books_authors_table(cls):
    #    return Table(cls.__name__ + '_books_authors', Base.metadata, Column('book_id', Integer, ForeignKey('book.id')), Column('author_id', Integer, ForeignKey('author.id')) )

class GenericBookDescription(object):
    id = Column(Integer, primary_key=True)
    @declared_attr
    def __tablename__(cls):
        registered[cls.__name__]=cls
        return cls.__name__
    @declared_attr
    def book_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__[:-len("Description")]+'.id'))
    description = Column(Unicode(20000))

    def __init__(self, initial_data):
        try:
            self.description = initial_data['description']
        except:
            exit('Record ' + initial_data + ' doesn\'t have defined desription')

