from generic import XMLConnector
from xml.etree import ElementTree as et
import os

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

    def parse(self):
        filename = os.path.join(self.unpack_dir,self.unpack_file)
        root = et.parse(filename).getroot()
        offers = list(root[0])
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic


   
