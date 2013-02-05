from generic import GenericConnector
import os

class XMLConnector(GenericConnector):

    UNKNOWN = -1
    SINGLE_XML = 0
    ZIPPED_XMLS = 1
    GZIPPED_XMLS = 2
    MULTIPLE_XMLS = 3

    _mode_dict = {'SINGLE_XML':SINGLE_XML,
                  'ZIPPED_XMLS':ZIPPED_XMLS,
                  'GZIPPED_XMLS':GZIPPED_XMLS,
                  'MULTIPLE_XMLS':MULTIPLE_XMLS }

    xml_tag_dict = {}

    def mode_int(self, mode):
        return self._mode_dict.get(mode,self.UNKNOWN) 

    def __init__(self,limit_books=0):
        GenericConnector.__init__(self)
        self.mode = self.mode_int(self.config['mode'])
        self.limit_books = limit_books
         
    def fetchData(self,unpack = True):
        self.downloadFile()
        if unpack:
            if self.mode == XMLConnector.ZIPPED_XMLS:
                self.unpackZIP(os.path.join(self.backup_dir,self.filename))
            elif self.mode == XMLConnector.GZIPPED_XMLS: 
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
