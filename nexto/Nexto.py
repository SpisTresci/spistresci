from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import urllib, urllib2


class Nexto(XMLConnector):

    url = "https://www.nextoapi.pl/download_xml.req"


    def __init__(self):
        XMLConnector.__init__(self, self.url, XMLConnector.ZIPPED_XMLS)
        
    def downloadFile(self, url):
        values = {'api_id': 'ZDhlODFkYjctNzYyZC00YTZjLTlkOTgtMTY4NDRhMDYwNDlm',
             'pass': 'pomyslowo42', 
             'xmlType':'PRODUCTS_LIST',}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        rsp = urllib2.urlopen(req)
        content = rsp.read()
        
        open("download_xml.gz", "wb").write(content)
        return "download_xml.gz"
        
    def parse(self):
                 
        filename  = 'download_xml'
        if not os.path.exists(filename):
            exit(-1)
 
        root = et.parse(filename).getroot()
        
        for product in root[0]:
            id          = product.find('id')
            isbn        = product.find('isbn')
            language    = product.find('language')
            description = product.find('body')
            title       = product.find('title')
            publisher   = product.find('publisher')
            manufacturer_id = product.find('manufacturer_id')

            print "Tytul: " + title
            print "ID: " + id
            print "Opis: " + description
            
        
def main():
    
        nexto = Nexto()
        
        nexto.fetchData()
        nexto.parse()
        #konektor.update()
        

if __name__ == '__main__':
    main()
