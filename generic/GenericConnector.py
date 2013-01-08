import abc

import urllib2
import zipfile
import gzip
import os.path


class GenericConnector(object):
    #__metaclass__ = abc.ABCMeta
    
    url = ""

    max_len = []
    max_len_entry = []
    
    def __init__(self, url):
        self.url = url
        print "GenericConnector Constructor!"
        

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
                self.max_len.append(len(list[i]))
                self.max_len_entry.append(list[i])
        else:
            for i in range(len(list)):
                if list[i] != None and self.max_len[i] < len(list[i]):
                    self.max_len[i] = len(list[i])
                    self.max_len_entry[i] = list[i]

    def downloadFile(self, url):
        
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        
        print "File last modified: " + meta.getheaders("Last-Modified")[0]
        print "Downloading: %s Bytes: %s" % (file_name, int(meta.getheaders("Content-Length")[0]))
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)
        
            #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            #status = status + chr(8)*(len(status)+1)
            #print status,

        f.close()
        return file_name

    def unpackGZIP(self, gzipname):
        fh = gzip.GzipFile(gzipname, "r")
        
        file_content = fh.read()
        fh.close()
        
        fileName, ext = os.path.splitext(gzipname)
        
        file = open(fileName, "w")
        file.write(file_content)
        file.close()
        
    def unpackZIP(self, zipname):
        zfile = zipfile.ZipFile(zipname)
        for name in zfile.namelist():
            (dirname, filename) = os.path.split(name)
        
            if dirname == "":
                dirname = zipname.split(".")[0]
        
            print "Decompressing " + filename + " on " + dirname
            if not os.path.exists(dirname) and dirname != "":
                os.mkdir(dirname)
            fd = open(dirname + os.sep + name,"w")
            fd.write(zfile.read(name))
            fd.close()
    
