from generic import XMLConnector

import os
import re
from xml.dom import minidom


class Virtualo(XMLConnector):
    
    
    url = "https://virtualo.pl/data/cennik_full.zip"
    
    def __init__(self):
        XMLConnector.__init__(self, self.url, XMLConnector.ZIPPED_XMLS)
    
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
    
            filename  = 'cennik_full' + os.sep + 'VirtualoProducts' + str(i) +'.xml'
            if not os.path.exists(filename):
                break
            
            self.removeDescriptionShortTag(filename)
            DOMTree = minidom.parse(filename)
            #print DOMTree.toxml()
    
            products = DOMTree.childNodes.item(0).childNodes
    
    
            print "START =======" + 'VirtualoProducts' + str(i) +'.xml' + "=========="
    
            for product in products:
                #product = products[103]
                title = self.getTagValue(product, 'title')
                format = self.getTagValue(product, 'format')
                security = self.getTagValue(product, 'security','brak')
                price = self.getTagValue(product, 'price')
                isbn = self.getTagValue(product, 'isbn')
                coverId = self.getTagValue(product, 'coverId')
                authors = self.getTagValue(product, 'authors')
                #print authors
    
                splitObj = re.split(', ', authors)
                if len(splitObj) != 1:
                    print authors
    
                url = self.getTagValue(product, 'url')
                description = self.getTagExpliciteValue(product, 'description')
                #descriptionShort = getTagValue(product, 'descriptionShort')
                rating = self.getTagValue(product, 'rating')
    
                #http://virtualo.pl/kodeks_karny_kodeks_postepowania_karnego_kodeks_karny/i123959/
                matchObj = re.match(r'.*/i(\d*)/', url)
                id = int(matchObj.group(1))
    
    
                #format_tag = product.getElementsByTagName('format')[0]
                #format = ""
                #if format_tag.firstChild != None:
                #      format = format_tag.firstChild.nodeValue
    
    
                #format = product.getElementsByTagName('format')[0].firstChild.nodeValue
    
                #security = product.getElementsByTagName('security')[0].firstChild.nodeValue
    
            print "END   =======" + 'VirtualoProducts' + str(i) +'.xml' + "=========="
            print "odczytano " + str(len(products)) + " produktow"
            i=i+1
    
        pass
            
