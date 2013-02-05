from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import sys
class Selkar(XMLConnector):
    
    def __init__(self,limit_books=0):
        XMLConnector.__init__(self,limit_books)
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

        'id':'id',
        'url':'url',
        'title':'title',
        'author':'author',
        'translator':'translator',
        'image':'cover',
        'published':'publication_date',
        'publisher':'publisher',
        'pages':'page_count',
        'dimensions':'size',
        'cover':'binding',
        'isbn':'isbn',
        'ean':'ean',
        'description':'description',
        #1 - available, 0 -not available
        'status':'status',
        'price':'price',
        'list_price':'list_price',
        'category_id':'category',
        'bestseller':'is_bestseller',
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
                print dic

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

