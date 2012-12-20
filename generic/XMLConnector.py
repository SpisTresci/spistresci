from generic.GenericConnector import GenericConnector
import os

class XMLConnector(GenericConnector):

    SINGLE_XML = 0;
    ZIPPED_XMLS = 1

    mode = -1

    def __init__(self, url, mode):
        GenericConnector.__init__(self, url)
        self.mode = mode
        print "XMLConnector Constructor!"
        
    
    def fetchData(self):
        if self.mode == XMLConnector.SINGLE_XML:
            self.downloadFile(self.url)

        elif self.mode == XMLConnector.ZIPPED_XMLS:
            zipname = self.downloadFile(self.url)
            
            fileName, ext = os.path.splitext(zipname)
            if ext == ".zip":
                self.unpackZIP(zipname)
            elif ext == ".gz":
                self.unpackGZIP(zipname)

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