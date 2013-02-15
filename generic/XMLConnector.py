from generic import GenericConnector
from utils import Enum
import os

class XMLConnector(GenericConnector):

    class XML_Mode(Enum):
        values = [
            'UNKNOWN',
            'SINGLE_XML',
            'ZIPPED_XMLS',
            'GZIPPED_XMLS',
            'MULTIPLE_XMLS',
        ]

    xml_tag_dict = {}


    def __init__(self, name=None, limit_books=0):
        GenericConnector.__init__(self, name=name)
        self.mode = self.XML_Mode.int(self.config.get('mode','UNKNOWN'))
        self.limit_books = limit_books
         
    def fetchData(self,unpack = True):
        self.downloadFile()
        if unpack:
            if self.mode == XMLConnector.XML_Mode.ZIPPED_XMLS:
                self.unpackZIP(os.path.join(self.backup_dir,self.filename))
            elif self.mode == XMLConnector.XML_Mode.GZIPPED_XMLS: 
                self.downloadFile()
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

    def make_dict(self,book):
        book_dict = {}
        for tag in self.xml_tag_dict.keys():
            tag_split = tag.split('.')
            if len(tag_split) > 1:
                sub_elem = book    
                for spl in tag_split:
                     sub_elem = sub_elem.find(spl)
                     if sub_elem is None:
                         break
                if sub_elem is not None:
                     sub_elem=sub_elem.text
                book_dict[ self.xml_tag_dict[tag] ]= sub_elem
            else:
                book_dict[ self.xml_tag_dict[tag] ] = book.findtext(tag) 
        return book_dict
