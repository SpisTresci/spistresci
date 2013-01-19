from generic import XMLConnector
from xml.etree import ElementTree as et
import os

#TODO: what to do with more than one elements with the same tagname?
class Helion(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'isbn':'isbn',
        'ean':'ean',
        'ident':'id',
        'tytul':'title',
        'link':'url',
        'autor':'author',
        'tlumacz':'translator',
        'status':'status',
        'cena':'price',
        'cenadetaliczna':'final_price',
        'znizka':'discount',
        'marka':'bookshop',
        'nazadanie':'on_demand',
        'format':'size',
        'typ':'type',
        'oprawa':'binding',
        'liczbastron':'page_count',
        'datawydania':'publication_date',
        'oinline':'online',
        'okladka':'cover',
        'bestseller':'is_bestseller',
        'nowosc':'is_new',
        'powiazane':'linked',
        'seriewydawnicze':'series',
        'serietematyczne':'thematic_series',
        'ksiegarnie_nieinter':'offline_bookshop',
        'opis':'description',
        'md5':'md5',
        'online':'online',
        'ident_powiazany':'lined_id',
        'seriawydawnicza':'series_id',
        'seriatematyczna':'thematic_series_id',
        'waga':'mass',
        'status2':'status2',
        'cena_netto':'net_price',
        'cena_brutto':'gross_price',
        'vat':'vat',
        'vat_procent':'vat_percent',
        'okladkatyl':'cover_back',
        'issueurl':'issueurl',
        'top':'top',
        'nosnik':'nosnik',
        'przedsprzedazDO':'advanced_booking',
        'ebook_format':'ebook_format',
        'ebook_formaty':'ebook_format_list'
    }


    def make_dict(self,elem):
        elem_dict = {}
        for child_elem in elem:
            child = self.make_dict(child_elem)
            if not child:
                child = child_elem.text
            #here an exception will be raised if we dont know this tag 
            #i.e. tag not in xml_tag_dict
            tag_name = self.xml_tag_dict[child_elem.tag]

            #TODO: what to do with more than one elements with the same tagname?

            ##isn't that a better approach?
            #i = 0
            #while tag_name in elem_dict:
            #    if i:
            #        tag_name = tag_name[:-1]
            #    tag_name += str(i)
            #    i+=1
            if tag_name in elem_dict:
                old_child = elem_dict[tag_name]
                if type(old_child) == list:
                    old_child.append(child)
                    child = old_child
                else:
                    child = [old_child,child]

            elem_dict[tag_name] = child
        if not len(elem_dict):
            return elem.text
        return elem_dict
            
    def __init__(self, limit_books=0):
        XMLConnector.__init__(self)
        self.limit_books = limit_books
      
    def parse(self):
        filename = os.path.join(self.unpack_dir,self.unpack_file)
        root = et.parse(filename).getroot()
        for base in root:
            if self.limit_books:
                base=base[:self.limit_books]
            for book in base:
                book_dict = self.make_dict(book)
                print book_dict
#            print "Tytul: ",book_dict['title']
#            print "ID: ", book_dict['id']
#            print "Opis: ", book_dict['description']
#            print "url: ",book_dict['url']
#            print 

   
