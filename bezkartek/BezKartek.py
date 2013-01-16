from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import traceback

class BezKartek(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'isbn':'isbn',
        'ebookId':'id',
        'name':'title',
        'url':'url',
        'authors':'author',
        'category':'category',
        'description':'description',
        'format':'format',
        'image':'cover',
        'languages.lang_short':'lang_short',
        'languages.lang_long': 'lang_long',
        'price':'price',
        'pageCount':'page_count',
        'publisher':'publisher',
        'securityType':'security',
        'audioTime':'audio_time',
    }


    def __init__(self, limit_books=0):
        XMLConnector.__init__(self)
        self.limit_books = limit_books
        
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
        filename = os.path.join(self.unpack_dir,self.unpack_file)
        root = et.parse(filename).getroot()
        offers = list(root[0])
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic


   
