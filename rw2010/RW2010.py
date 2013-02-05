from generic import XMLConnector
from xml.etree import ElementTree as et
import urllib2
import os

class RW2010(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'tytul':'title',
        'url':'url',
        'autor':'author',
        'formaty':'format',
        'okladka':'cover',
        'cena':'price',
    }

    def __init__(self, limit_books=0):
        XMLConnector.__init__(self, limit_books)
        self.macro_url = self.config['macro_url']
        u = urllib2.urlopen(self.macro_url) 
        meta = u.info()
        result = u.read()
        u.close()
        if result!= 'Ok.':
            raise Exception('RW2010 init, macro %s returned %s'%(self.macro_url,result))

    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic


   
