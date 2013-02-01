import os
from generic import *
from xml.etree import ElementTree as et
from sql_wrapper import *

class BezKartek(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'isbn':'isbn',
        'ebookId':'external_id',
        'name':'title',
        'url':'url',
        'authors':'authors',
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
        book_dict['authors']=[x.strip() for x in book_dict['authors'].split(',')] #TODO: strip
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
            self.add_record(dic)


Base = SqlWrapper.getBaseClass()

class BezKartekBook(GenericBook, Base):
    id =  Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    category = Column(Unicode(100))

class BezKartekBookDescription(GenericBookDescription, Base):
    pass

class BezKartekAuthor(GenericAuthor, Base):
    pass


