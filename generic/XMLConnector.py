from generic import GenericConnector
import os

class XMLConnector(GenericConnector):

    UNKNOWN = -1
    SINGLE_XML = 0
    ZIPPED_XMLS = 1
    GZIPPED_XMLS = 2

    _mode_dict = {'SINGLE_XML':SINGLE_XML,
                  'ZIPPED_XMLS':ZIPPED_XMLS,
                  'GZIPPED_XMLS':GZIPPED_XMLS }

    def mode_int(self, mode):
        return self._mode_dict.get(mode,self.UNKNOWN) 

    def __init__(self,limit_books=0):
        GenericConnector.__init__(self)
        self.mode = self.mode_int(self.config['mode'])
        self.limit_books = limit_books
         
    def fetchData(self):
        self.downloadFile()
        if self.mode == XMLConnector.ZIPPED_XMLS:
            self.unpackZIP(os.path.join(self.backup_dir,self.filename))
        elif self.mode == XMLConnector.GZIPPED_XMLS: 
            self.unpackGZIP(os.path.join(self.backup_dir,self.filename))

    def getTagValue(self, product, tagName, default=""):
        tag = product.getElementsByTagName(tagName)[0]
        value_of_tag = default
        if tag.firstChild != None:
            value_of_tag = tag.firstChild.nodeValue
        return value_of_tag
    
    def getTagExpliciteValue(self, product, tagName, default=""):

        tag = product.getElementsByTagName(tagName)[0]
        value_of_tag = default
        if tag.firstChild != None:
            value_of_tag = tag.toxml()
        return value_of_tag[len(('<'+tagName+'>')):-len(('</'+tagName+'>'))]
