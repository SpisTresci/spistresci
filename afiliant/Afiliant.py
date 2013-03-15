from generic import XMLConnector
from xml.etree import ElementTree as et
from generic import *
import os

class Afiliant(XMLConnector):
    
    
    #dirty hack,
    #probably will have to fix that in the future using
    #et._namespace_map[''] = ''
    xmls_namespace = '{urn:ExportB2B}'

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        xmls_namespace+'id':('external_id',''),
        xmls_namespace+'name':('title',''),
        xmls_namespace+'url':('url',''),
        xmls_namespace+'categoryId':('category',''),
        xmls_namespace+'description':('description',''),
        xmls_namespace+'image':('cover',''),
        xmls_namespace+'price':('price', 0),
    }
    
    xml_attributes_dict = {
        'Autor':('authors',''),
        'ISBN':('isbn',''),
        'Wydawnictwo':('publisher',''),
        'Rok_wydania':('year',''),
        'Format':('format',''),
        'Wydawca':('publisher',''),
        'Czyta':('lector',''),
        u'Dugo\u015b\u0107':('length',''),
        'Producent':('manufacturer',''),

    }

    def make_dict(self,book):
        book_dict = {}
        for tag in self.xml_tag_dict.keys():
            book_dict[ (self.xml_tag_dict[tag])[0] ] = unicode(book.findtext(tag, (self.xml_tag_dict[tag])[1] ))

        attributes = book.find(self.xmls_namespace+'attributes')

        if not attributes:
            return book_dict

        for attribute in attributes:
            name = attribute.findtext(self.xmls_namespace+'name')
            value = unicode(attribute.findtext(self.xmls_namespace+'value', (self.xml_attributes_dict[name])[1]))
            book_dict_key = (self.xml_attributes_dict[name])[0]
            if book_dict_key in book_dict:
                raise KeyError('%s already in book_dict'%book_dict_key)
            book_dict[book_dict_key]=value
        return book_dict


    def parse(self):
        filename = os.path.join(self.backup_dir,self.filename)
        root = et.parse(filename).getroot()
        body = root[0]
        loadoffers = body[0]
        offerstag = loadoffers[0]
        offers=list(offerstag)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            print dic


class AfiliantBook(GenericBook):
    pass

class AfiliantBookDescription(GenericBookDescription):
    pass

class AfiliantAuthor(GenericAuthor):
    pass

class AfiliantBookPrice(GenericBookPrice):
    pass

class AfiliantBooksAuthors(GenericBooksAuthors):
    pass

#TODO: what to do with "Opracowanie: 'Name'" Producers (authors)
class ZielonaSowa(Afiliant):pass

class ZloteMysli(Afiliant):

    xml_attributes_dict = {
        'Autor':'author',
        'ISBN':'isbn',
        'Wydawnictwo':'publisher',
        'Rok wydania':'year',
        'Format':'format',
        'Format pliku':'ebook_format',
        u'Ilo\u015b\u0107 stron':'length',
        'Oprawa':'binding',
        #it may be sth different than image tag
        'zm:imageParent':'cover_zm',
        'zm:imageMedium':'cover_medium',
        'zm:imageSmall':'cover_small',
        #it may be sth different than category
        'zm:categoryId':'category_zm',
        'zm:productTypeId':'product_type',
    }
