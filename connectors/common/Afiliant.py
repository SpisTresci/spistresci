from connectors.generic import XMLConnector
import lxml.etree as et
from connectors.generic import *
import os

class Afiliant(XMLConnector):

    #dirty hack,
    #probably will have to fix that in the future using
    #et._namespace_map[''] = ''
    xmls_namespace = '{urn:ExportB2B}'

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': (xmls_namespace + 'id', ''),
        'title': (xmls_namespace + 'name', ''),
        'url': (xmls_namespace + 'url', ''),
        'category': (xmls_namespace + 'categoryId', ''),
        'description': (xmls_namespace + 'description', ''),
        'cover': (xmls_namespace + 'image', ''),
        'price': (xmls_namespace + 'price', 0),
    }

    xml_attributes_dict = {
        'Autor':('authors', ''),
        'ISBN':('isbn', ''),
        'Wydawnictwo':('publisher', ''),
        'Rok_wydania':('year', ''),
        'Format':('format', ''),
        'Wydawca':('publisher', ''),
        'Czyta':('lectors', ''),
        u'Dugo\u015b\u0107':('length', ''),
        'Producent':('manufacturer', ''),

    }

    def make_dict(self, book):
        book_dict = {}
        for tag in self.xml_tag_dict.keys():
            book_dict[ tag ] = unicode(book.findtext( (self.xml_tag_dict[tag])[0], (self.xml_tag_dict[tag])[1]))

        attributes = book.find(self.xmls_namespace + 'attributes')

        if not attributes:
            return book_dict

        for attribute in attributes:
            name = attribute.findtext(self.xmls_namespace + 'name')
            value = unicode(attribute.findtext(self.xmls_namespace + 'value', (self.xml_attributes_dict[name])[1]))
            book_dict_key = (self.xml_attributes_dict[name])[0]
            if book_dict_key in book_dict:
                raise KeyError('%s already in book_dict' % book_dict_key)
            book_dict[book_dict_key] = value
        return book_dict


    def parse(self):
        filename = os.path.join(self.backup_dir, self.filename)
        root = et.parse(filename).getroot()
        body = root[0]
        loadoffers = body[0]
        offerstag = loadoffers[0]
        offers = list(offerstag)
        if self.limit_books:
            offers = offers[:self.limit_books]
        for book in offers:
            dic = self.make_dict(book)
            self.validate(dic)
            self.add_record(dic)
