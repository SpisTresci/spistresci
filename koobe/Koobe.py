from generic import XMLConnector
from xml.etree import ElementTree as et
import os


class Koobe(XMLConnector):
    
    url = "http://www.koobe.pl/export/ekundelek.xml"
    
    def __init__(self):
        XMLConnector.__init__(self, self.url, XMLConnector.SINGLE_XML)
        
    def parse(self):
                
        filename  = 'ekundelek.xml'
        if not os.path.exists(filename):
            exit(-1)
 
        root = et.parse(filename).getroot()
        
        for product in root[0]:
            title = product.find('name').text
            id = product.find('id').text
            description = product.find('description').text
            url = product.find('url').text
            image = product.find('image').text
            price = product.find('price').text
            category = product.find('category').text
            producer = product.find('producer').text
            
            print "Tytul: " + title
            print "ID: " + id
            print "Opis: " + description
            print "url: " + url + "\n"
