from generic import GenericConnector
from utils import Enum
import os

class XMLConnector(GenericConnector):

    xml_tag_dict = {}

    def __init__(self, name=None, limit_books=0):
        GenericConnector.__init__(self, name=name)
        self.limit_books = limit_books
         
    def fetchData(self,unpack = True):
        self.downloadFile()
        if unpack:
            if self.mode == XMLConnector.BookList_Mode.ZIPPED_XMLS:
                self.unpackZIP(os.path.join(self.backup_dir,self.filename))
            elif self.mode == XMLConnector.BookList_Mode.GZIPPED_XMLS: 
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
                     sub_elem=unicode(sub_elem.text)
                book_dict[ (self.xml_tag_dict[tag])[0] ]= sub_elem
            else:
                book_dict[ (self.xml_tag_dict[tag])[0] ] = unicode(book.findtext(tag, (self.xml_tag_dict[tag])[1] ))
        return book_dict
