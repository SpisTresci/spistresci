import os
from generic import *
from xml.etree import ElementTree as et
from sql_wrapper import *

class BezKartek(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'isbn':('isbn', ''),
        'ebookId':('external_id', None),
        'name':('title', ''),
        'url':('url', None),
        'authors':('authors', ''),
        'category':('category', ''),
        'description':('description', ''),
        'format':('format',''),
        'image':('cover', ''),
        'languages.lang_short':('lang_short',''),
        'languages.lang_long': ('lang_long',''),
        'price':('price', 0),
        'pageCount':('page_count', 0),
        'publisher':('publisher', ''),
        'securityType':('security', ''),
        'audioTime':('audio_time',''),
    }


    def parse(self):
        filename = os.path.join(self.unpack_dir,self.unpack_file)
        root = et.parse(filename).getroot()
        offers = list(root[0])
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            self.validate(dic)
            #print dic
            #self.mesureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])


Base = SqlWrapper.getBaseClass()

class BezKartekBook(GenericBook, Base):
    id =  Column(Integer, primary_key=True)

    category = Column(Unicode(30))      #29

    audio_time = Column(Unicode(10))    #9
    isbn = Column(Unicode(30))          #27, 978-83-63444-25-9/1895-247X
    format = Column(Unicode(4))         #4
    price = Column(Integer)             #GROSZE!!!
    page_count = Column(Integer)        #508700 - wtf?
    publisher = Column(Unicode(70))     #68
    url = Column(Unicode(270))          #265
    cover = Column(Unicode(256))        #184
    security = Column(Unicode(10))      #9
    lang_short = Column(Unicode(2))     #2
    lang_long = Column(Unicode(10))     #9


class BezKartekBookDescription(GenericBookDescription, Base):
    pass

class BezKartekAuthor(GenericAuthor, Base):
    pass

class BezKartekBookPrice(GenericBookPrice, Base):
    pass

class BezKartekBooksAuthors(GenericBooksAuthors, Base):
    pass

