from generic import XMLConnector

import os
import re
from xml.dom import minidom

class Virtualo(XMLConnector):
    
    
    
    def __init__(self):
        XMLConnector.__init__(self)
    
    def removeDescriptionShortTag(self, filename):
        """
        This is done because of bug T25. DescriptionShort tags very often contain within itself unclosed formating tags.
        Because information which is in descriptionShort is redundand (we have to keep full description anyway), so we can remove this tag from xmls.
        """
    
        ifile = open(filename,'r',)
        text = ifile.read()
        ifile.close()
    
        text = re.sub(r'(<descriptionShort>.*?</descriptionShort>)',r'', text, 0, re.DOTALL| re.MULTILINE | re.VERBOSE)
    
        file_times = open(filename,"w")
        file_times.write(text)
        file_times.close()
        

        
    def parse(self):
        
        i=1
    
        while True:
            filename  = 'VirtualoProducts' + str(i) +'.xml'
            filename = os.path.join(self.unpack_dir,filename)
            if not os.path.exists(filename):
                break
            
            self.removeDescriptionShortTag(filename)
            DOMTree = minidom.parse(filename)
    
            products = DOMTree.childNodes.item(0).childNodes
    
            self.logger.debug('Parsing %s'%os.path.split(filename)[1])
    
            for product in products:
                title = self.getTagValue(product, 'title')
                format = self.getTagValue(product, 'format')
                security = self.getTagValue(product, 'security','brak')
                price = self.getTagValue(product, 'price')
                isbn = self.getTagValue(product, 'isbn')
                coverId = self.getTagValue(product, 'coverId')
                authors = self.getTagValue(product, 'authors')
                #print authors
                #splitObj = re.split(', ', authors)
                #if len(splitObj) != 1:
                #    print authors
    
                url = self.getTagValue(product, 'url')
                description = self.getTagExpliciteValue(product, 'description')
                rating = self.getTagValue(product, 'rating')
    
                matchObj = re.match(r'.*/i(\d*)/', url)
                id = int(matchObj.group(1))
    
    
                #format_tag = product.getElementsByTagName('format')[0]
                #format = ""
                #if format_tag.firstChild != None:
                #      format = format_tag.firstChild.nodeValue
    
    
                #format = product.getElementsByTagName('format')[0].firstChild.nodeValue
    
                #security = product.getElementsByTagName('security')[0].firstChild.nodeValue
    
            self.logger.debug('File %s parsed'%os.path.split(filename)[1])
            self.logger.debug('Virtualo, read %d products'%len(products))
            i=i+1
        
        pass

            
