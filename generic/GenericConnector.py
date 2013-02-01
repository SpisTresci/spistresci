import urllib2
import zipfile
import gzip
import os.path
import ConfigParser
from datetime import datetime
import shutil

from connectors_logger import logger_instance

class GenericConnector(object):
    
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
    def my_name(cls):
        return cls.__name__


    name = property(lambda x:x.my_name())

    def _parse_config(self, config_file='conf/connectors.ini', section=None, config_object = None):
        if not config_object:
            self.read_config()
        else:
             self.config_object = config_object
        if not section:
           section = self.my_name()
        self.section = section

        self.config = dict(self.config_object.items(self.section,
                        vars={'date':datetime.now().strftime('%Y%m%d%H%M%S')}
                      ))
        
    def __init__(self):
        self._parse_config(self.config_file, config_object=self.config_object)
        self.url = self.config['url']
        self.filename = self.config['filename']
        self.backup_dir = self.config.get('backup_dir', '')
        self.remove_backup = int(self.config.get('remove_backup', 1))
        self.unpack_file = self.config.get('unpack_file', '')
        self.unpack_dir = self.config.get('unpack_dir', '')
        self.remove_unpacked = int(self.config.get('remove_unpacked', 1))
        self.log_config=self.config.get('log_config', 'conf/log.connectors.ini')
        self.logger = logger_instance(self.log_config)
        self.logger.debug('%s connector created'%self.name)
  
    def __del__(self):
        if self.backup_dir and self.remove_backup and os.path.exists(self.backup_dir):
            cwd = os.getcwd().rstrip('/')+'/'
            abs_path = os.path.abspath(self.backup_dir).rstrip('/')+'/'
            if abs_path in cwd:
                raise IOError('Are you insane or something?. Don\'t tell me to remove whole my working dir\nHINT:backup_dur should not be current dir or parent')
            self.logger.debug('Connector %s. Removing backup dir %s'%(self.name,self.backup_dir))
            shutil.rmtree(self.backup_dir)
            self.backup_dir=''
        if self.unpack_dir and self.remove_unpacked and os.path.exists(self.unpack_dir):
            abs_path = os.path.abspath(self.unpack_dir).rstrip('/')+'/'
            if abs_path in cwd:
                raise IOError('Are you insane or something?. Don\'t tell me to remove whole my working dir\nHINT:unpack_dir should not be current dir or parent')
            self.logger.debug('Connector %s. Removing unpack dir %s'%(self.name,self.backup_dir))
            shutil.rmtree(self.unpack_dir)
            self.unpack_dir=''

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

    def downloadFile(self):
        u = urllib2.urlopen(self.url)
        if self.backup_dir and not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        filename = os.path.join(self.backup_dir, self.filename)
        f = open(filename, 'wb')
        meta = u.info()
        if meta.getheader("Content-Length"):
            self.logger.info('%s connector, downloading %s into %s (%s bytes)' % 
            (self.name, self.filename, self.backup_dir, int(meta.getheader('Content-Length'))))
        else:
            self.logger.info('%s connector downloading %s into %s'%(self.name, self.filename,self.backup_dir))
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
        self.logger.debug('Download of %s completed, downloaded %d bytes'%(self.filename,file_size_dl))
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
       
    
