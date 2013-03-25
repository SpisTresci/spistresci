from generic import *
from xml.etree import ElementTree as et
import os
import sys
from sql_wrapper import *

class Selkar(XMLConnector):
    
    def __init__(self, name=None, limit_books=0):
        print 'PZ selkar __init__ config_file = %s, config_object = %s' % (self.config_file, self.config_object)
        XMLConnector.__init__(self,name=name,limit_books=limit_books)
        self.api_key = self.config['api_key']
        self.method = self.config.get('method','getProduct')
        self.aff=self.config['aff']
        self.limit=int(self.config.get('limit',5000))
        categories = str(self.config.get('categories',''))
        self.categories = categories.split(',')
        self.fetched_xmls = {} 
    
    def _is_last(self,root):
        items = root.find('items')
        attrs = items.attrib
        page = int(attrs.get('page',1))
        total = int(attrs.get('totalPages',0))
        return page >= total

    def _make_url(self, params,category=None):
        ret_url = '%(url)s?apiKey=%(api_key)s&method=%(method)s&aff=%(aff)s&limit=%(limit)d&page=%(page)d'%params
        if category:
            ret_url=ret_url+'&cid=%s'%category
        return ret_url

    xml_tag_dict= {

        'id':('external_id',''),
        'url':('url',''),
        'title':('title',''),
        'author':('authors',''),
        'translator':('translators',''),
        'image':('cover',''),
        'published':('publication_date',''),
        'publisher':('publisher',''),
        'pages':('page_count',0),
        'dimensions':('size',''),
        'cover':('binding',''),
        'isbn':('isbn',''),
        'ean':('ean',''),
        'description':('description',''),
        #1 - available, 0 -not available
        'status':('status',''),
        'price':('price',0),
        'list_price':('list_price',0),
        'category_id':('category',''),
        'bestseller':('is_bestseller',''),
    }

    def parse(self):
        for (key, root) in self.fetched_xmls.items():
            itemstag = root.find('items')
            if itemstag:
                items= list(itemstag)
            else:
                items = []
            if self.limit_books:
                itemss = items[:self.limit_books]
            for book in items:
                dic = self.make_dict(book)
                #print dic
                self.validate(dic)
                #print dic
                #self.measureLenghtDict(dic)
                self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])


    def applySingleFilter(self, filterClass):
        raise NotImplementedError('One Does Not Simply apply filter on Selkar without implementation')

    def fetchData(self, unpack=True):
        params = {'url':self.url,
            'api_key':self.api_key,
            'method':self.method,
            'aff':self.aff,
            'limit':self.limit,
            'page':1}

        i = 0
        for category in self.categories:
            page = 1
            last_file = False
            while not last_file:
                params['page'] = page
                filename = '%s%d.xml'%(self.filename,i)
                url = self._make_url(params,category)
                fetched_file= self.downloadFile(url,filename)
                root = et.parse(fetched_file).getroot()
                self.fetched_xmls[fetched_file] = root
                last_file = self._is_last(root)
                i+=1
                page+=1

    def validate(self, dic):
        XMLConnector.validate(self, dic)

        id=dic.get('external_id')
        title=dic.get('title')
        self.validatePrice(dic, id, title, 'list_price')
        self.validateAuthors(dic, id, title, 'translators')

Base = SqlWrapper.getBaseClass()

class SelkarBook(GenericBook, Base):
    status = Column(Boolean)
    isbn = Column(Unicode(13))          #13
    publication_date = Column(Date)
    ean = Column(Unicode(13))           #15
    price = Column(Integer)             #GROSZE!!!
    page_count = Column(Integer)
    binding = Column(Unicode(25))       #22
    #translators
    is_bestseller = Column(Boolean)
    #authors
    list_price = Column(Integer)        #GROSZE!!!
    #external_id
    category = Column(Integer)
    publisher = Column(Unicode(60))     #57
    url = Column(Unicode(180))          #173
    cover = Column(Unicode(80))         #66

class SelkarBookDescription(GenericBookDescription, Base):
    pass

class SelkarAuthor(GenericAuthor, Base):
    pass

class SelkarBookPrice(GenericBookPrice, Base):
    pass

class SelkarBooksAuthors(GenericBooksAuthors, Base):
    pass

#{'status': 1, 'isbn': 13, 'description': 8000, 'publication_date': 10, 'ean': 15, 'price': 5, 'page_count': 4,
# 'binding': 22, 'translator': 92, 'is_bestseller': 1, 'authors': 10, 'list_price': 6, 'id': 6, 'size': 32, 'category': 4, 'publisher': 57, 'title': 100, 'url': 173, 'cover': 66}
#status: 1
#category: 2716
#isbn: 9788377998229
#description:
#ean: 978830116510901
#url: http://selkar.pl/osobowosc-samorealizacja-kariera-2/trud-i-zmaganie-milosc-i-szczescie-skupienie-rekolekcyjne-o-milosci-samego-siebie-ksiazka-audio-c?aff=admin@spistresci.pl
#title:
#price: 11990
#page_count: 1254
#binding: Miekka ze skrzydelkami
#cover: http://selkar.pl/img/product_media/190001-191000/1014697365(1).jpg
#translator: Litwinow Jezry, Brzechwa Jan, Wyszomirski Jezry, Jastrzebiec-Kozlowski Czeslaw, Tuwim Julian
#is_bestseller: 0
#list_price: 199.00
#authors: [u'Tom Krause', u'Elizabeth Harwood', u'Mirella Freni', u'Jos\xe9 Van Dam', u'Frederica von Stade', u'Jane Barbi\xe9', u'Michel S\xe9n\xe9chal', u'et al.', u'vocal soloists/Vienna Philharmonic Orchestra & Chorus of the Vienna State Opera', u'/Herbert von Karajan']
#publisher: Firma Ksiegarska Jacek i Krzysztof Olesiejuk - Inwestycje
#publication_date: 2011-03-16
#id: 219838
#size: 1900.0000 x 1300.0000 x 190.0000

