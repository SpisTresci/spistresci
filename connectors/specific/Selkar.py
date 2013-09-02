from connectors.generic import XMLConnector
from connectors.Tools import notFilterableConnector
import lxml.etree as et
import os
import sys
from sqlwrapper import *
from connectors.generic import GenericBook

@notFilterableConnector
class Selkar(XMLConnector):

    def __init__(self, name = None, limit_books = 0):
        XMLConnector.__init__(self, name = name, limit_books = limit_books)
        self.api_key = self.config['api_key']
        self.method = self.config.get('method', 'getProduct')
        self.aff = self.config['aff']
        self.limit = int(self.config.get('limit', 5000))
        categories = str(self.config.get('categories', ''))
        self.categories = categories.split(',')
        self.fetched_xmls = {}

    def _is_last(self, root):
        items = root.find('items')
        attrs = items.attrib
        page = int(attrs.get('page', 1))
        total = int(attrs.get('totalPages', 0))
        return page >= total

    def _make_url(self, params, category = None):
        ret_url = '%(url)s?apiKey=%(api_key)s&method=%(method)s&aff=%(aff)s&limit=%(limit)d&page=%(page)d' % params
        if category:
            ret_url = ret_url + '&cid=%s' % category
        return ret_url

    #TODO: redefine xml dict, adjust to new makeDict
    xml_tag_dict = {

        'external_id': ('id', ''),
        'url': ('url', ''),
        'title': ('title', ''),
        'authors': ('author', ''),
        'translators': ('translator', ''),
        'cover': ('image', ''),
        'publication_date': ('published', ''),
        'publisher': ('publisher', ''),
        'page_count': ('pages', 0),
        'size': ('dimensions', ''),
        'binding': ('cover', ''),
        'isbn': ('isbn', ''),
        'ean': ('ean', ''),
        'description': ('description', ''),
        #1 - available, 0 -not available
        'status': ('status', ''),
        'price': ('price', 0),
        'list_price': ('list_price', 0),
        'category': ('category_id', ''),
        'is_bestseller': ('bestseller', ''),
    }

    def parse(self):
        for (key, root) in self.fetched_xmls.items():
            itemstag = root.find('items')
            if itemstag:
                items = list(itemstag)
            else:
                items = []
            if self.limit_books:
                itemss = items[:self.limit_books]
            for book in items:
                dic = self.makeDict(book)
                #print dic
                self.validate(dic)
                #print dic
                #self.measureLenghtDict(dic)
                self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])

    def fetchData(self, unpack = True):
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
                filename = '%s%d.xml' % (self.filename, i)
                url = self._make_url(params, category)
                fetched_file = self.downloadFile(url, filename)
                root = et.parse(fetched_file).getroot()
                self.fetched_xmls[fetched_file] = root
                last_file = self._is_last(root)
                i += 1
                page += 1

    def validate(self, dic):
        XMLConnector.validate(self, dic)

        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, 'list_price')

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
