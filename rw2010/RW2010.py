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
        XMLConnector.__init__(self)
        self.macro_url = self.config['macro_url']
        self.limit_books = limit_books
        u = urllib2.urlopen(self.macro_url) 
        meta = u.info()
        result = u.read()
        u.close()
        if result!= 'Ok.':
            raise Exception('RW2010 init, macro %s returned %s'%(self.macro_url,result))
        
    def make_dict(self,book):
        book_dict = {}
        for tag in self.xml_tag_dict.keys():
            tag_split = tag.split('.')
            if len(tag_split) > 1:
                sub_elem = book    
                for spl in tag_split:
                     sub_elem = sub_elem.find(spl)
                     if sub_elem is None:
                         break
                if sub_elem is not None:
                     sub_elem=sub_elem.text
                book_dict[ self.xml_tag_dict[tag] ]= sub_elem
            else:
                book_dict[ self.xml_tag_dict[tag] ] = book.findtext(tag) 
        return book_dict


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic


   
