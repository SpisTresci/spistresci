from generic import XMLConnector
from xml.etree import ElementTree as et
import urllib2
import os

class Czytio(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'id':'id',
        'title':'title',
        'url':'url',
        'authors':'author',
        'format':'format',
        'isbn':'isbn',
        'cover':'cover',
        'price':'price',
        'size':'size',
    }
    
    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        offers = list(root)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic

