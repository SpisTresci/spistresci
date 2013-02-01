from generic import XMLConnector
from generic import GenericBook
from generic import GenericBookDescription
from generic import GenericAuthor
from xml.etree import ElementTree as et
import os


class Koobe(XMLConnector):
    
    def __init__(self,name=None):
        XMLConnector.__init__(self, name=name)
        
    def parse(self):
                
        filename = os.path.join(self.backup_dir, self.filename)
        if not os.path.exists(filename):
            exit(-1)
 
        root = et.parse(filename).getroot()

        for product in root[0]:
            d={}
            d['title'] = product.findtext('name')
            d['external_id'] = product.findtext('id')
            d['description'] = product.findtext('description')
            d['url'] = product.findtext('url')
            d['image'] = product.findtext('image')
            d['price'] = product.findtext('price')
            d['category'] = product.findtext('category')
            d['producer'] = product.findtext('producer')

            d['isbn']=d['protection']=None
            d['authors']=[]
            d['format']=[]

            for property in product.findall('property'):
                if d['isbn'] == None:
                    if property.get('name') == 'isbn':
                        d['isbn'] = property.text

                if property.get('name') == 'author':
                    d['authors'].append(property.text)
                    
                if property.get('name') == 'format':
                    d['format'].append(property.text)

                if d['protection'] == None:
                    if property.get('name') == 'protection':
                        d['protection'] = property.text

            #print "Tytul: " + title
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
            # self.mesureLenght([title, id, description, url, image, price, category, producer, isbn, author, format, protection])
            #self.add_record({'external_id':1234, 'authors':['Jas Fasola'], 'description':'opis', 'title':'Taki sobie tytul', 'category':'horror'})
            self.add_record(d)

        print self.max_len
        for el in self.max_len_entry:
            print el

from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.ext.declarative import declared_attr
Base = declarative_base()
engine  = create_engine('mysql://root:Z0oBvgF1R3@localhost/st', echo=True)


class KoobeBook(GenericBook, Base):
    id =  Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    category = Column(Unicode(100))

class KoobeBookDescription(GenericBookDescription, Base):
    t = Column(Unicode(100))
    
class KoobeAuthor(GenericAuthor, Base):
    r = Column(Unicode(100))
    books = relationship(**KoobeBook.secondary_books_authors_table(Base))


engine  = create_engine('mysql://root:Z0oBvgF1R3@localhost/st', echo=True)    
Base.metadata.create_all(engine)

