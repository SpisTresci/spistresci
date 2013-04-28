from connectors.common import *
from connectors.generic import XMLConnector
from xml.etree import ElementTree as et
from sqlwrapper import *
import os

Base = SqlWrapper.getBaseClass()

class Latarnik(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        ".[@id]":('external_id', ''),
        ".[@url]":('url', ''),
        ".[@price]":('price', 0),
        ".[@avail]":('availability', ''),
        ".[@set]":('set', 0), #???
        ".[@stack]":('stack', 0), #???
        ".[@weight]":('weight', '0.00'),

        "./cat":('category', ''),
        "./name":('title', ''),
        "./imgs/main[@url]":('cover', ''),
        "./desc":('description', ''),
        #"":('authors', ''),  - autor jest umieszczony w drugim wierszu description
        #"":('nosnik', ''),  - nosnik jest umieszczony w czwartym wierszu description
        #"":('rozmiar', ''),  - rozmiar jest umieszczony w szostym wierszu description
        #"":('oprawa', ''),  - oprawa jest umieszczony w szostym wierszu description
        "./attrs/a[@name='EAN']":('isbn', ''),
        "./attrs/a[@name='Producent']":('publisher', ''),
        "./attrs/a[@name='Kod_producenta']":('publisher_code', ''),
    }

    def validate(self, dic):
        self.createFromDescription(dic, u"Autor", "authors")
        self.createFromDescription(dic, u"No\xc3nik", "form")
        self.createFromDescription(dic, u"Rozmiar", "form")
        self.createFromDescription(dic, u"Oprawa", "type")
        super(Latarnik, self).validate(dic)

    def createFromDescription(self, dic, name, tag):
        if dic.get('description') == None:
            return
        header_of_desc = dic['description'].split("\n\n\n")[0].split("\n")

        for i in range(0, len(header_of_desc), 2):
            if name + ":" in header_of_desc[i] and i <= len(header_of_desc) - 1 :
                dic[tag] = header_of_desc[i + 1]


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        group_books = root
        offers = list(group_books)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.makeDict(book)
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key + ": " + unicode(self.max_len_entry[key])


#{'publisher_code': 17, 'set': 1, 'isbn': 13, 'description': 4336, 'weight': 5, 'price': 4,
#'authors': 38, 'availability': 2, 'category': 22, 'publisher': 33, 'form': 7, 'title': 72, 'url': 104,
# 'external_id': 3, 'cover': 125, 'stack': 1, 'type': 30}


class LatarnikBook(CeneoBook, Base):
    id = Column(Integer, primary_key=True)

    url = Column(Unicode(128))          #104
    price = Column(Integer)             #GROSZE!!!
    availability = Column(Integer)      #2-"99"
    set = Column(Integer)               #1 - ???
    stack = Column(Unicode(2))          #1 - ???
    weight = Column(Unicode(8))         #5 - ???

    category = Column(Unicode(32))      #22
    title = Column(Unicode(128))        #72
    cover = Column(Unicode(256))        #256
    isbn = Column(Unicode(13))          #0
    publisher = Column(Unicode(64))     #33
    publisher_code = Column(Unicode(32))        #17

class LatarnikBookDescription(CeneoBookDescription, Base):
    pass

class LatarnikAuthor(CeneoAuthor, Base):
    pass

class LatarnikBookPrice(CeneoBookPrice, Base):
    pass

class LatarnikBooksAuthors(CeneoBooksAuthors, Base):
    pass

