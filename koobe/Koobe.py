from generic import XMLConnector
from xml.etree import ElementTree as et
import os


class Koobe(XMLConnector):
    
    def __init__(self):
        XMLConnector.__init__(self)
        
    def parse(self):
                
        filename = os.path.join(self.backup_dir, self.filename)
        if not os.path.exists(filename):
            exit(-1)
 
        root = et.parse(filename).getroot()

        for product in root[0]:
            title = product.findtext('name')
            id = product.findtext('id')
            description = product.findtext('description')
            url = product.findtext('url')
            image = product.findtext('image')
            price = product.findtext('price')
            category = product.findtext('category')
            producer = product.findtext('producer')

            isbn = author = format = protection = None


            for property in product.findall('property'):
                if isbn == None:
                    if property.get('name') == 'isbn':
                        isbn = property.text

                if author == None:
                    if property.get('name') == 'author':
                        author = property.text

                if format == None:
                    if property.get('name') == 'format':
                        format = property.text

                if protection == None:
                    if property.get('name') == 'protection':
                        protection = property.text

            print "Tytul: " + title
            # print "ID: " + id
            # print "Opis: " + description
            # print "url: " + url
            # print "image: " + image
            # print "price: " + price
            # print "category: " + category
            # print "producer: " + producer
            # print "isbn: " + isbn
            # print "author: " + author
            # print "format: " + format
            # print "protection: " + protection
            self.mesureLenght([title, id, description, url, image, price, category, producer, isbn, author, format, protection])


        print self.max_len
        for el in self.max_len_entry:
            print el

