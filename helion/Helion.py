from generic import XMLConnector
from xml.etree import ElementTree as et
import os
import traceback

#TODO: translate helion xml tags into some kind of standarized key in dict
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
        'znizka':'???promotion',
        'marka':'bookshop',
        'nazadanie':'on_demand',
        'format':'???form',
        'typ':'type',
        'oprawa':'???oprawa',
        'liczbastron':'num_pages',
        'datawydania':'??publish_date',
        'online':'online',
        'okladka':'???okladka',
        'bestseller':'is_bestseller',
        'nowosc':'is_new',
        'powiazane':'??linked',
        'seriewydawnicze':'series',
        'serietematyczne':'???topic_series',
        'ksiegarnie_nieinter':'offline_bookshop',
        'opis':'description',
        'md5':'md5',
    }


    def make_dict(self,elem):
        elem_dict = {}
        for child_elem in elem:
            child = self.make_dict(child_elem)
            if not child:
                child = child.text
            tag_name = self.xml_tag_dict.get(child_elem.tag,child_elem.tag)

            #TODO:what to do if there is more than one child elem with same tag

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
            
        
    def __init__(self):
        url = 'http://helion.pl/xml/produkty-wszystkie.xml.zip'
        XMLConnector.__init__(self, url, XMLConnector.ZIPPED_XMLS)
        
    def parse(self):
                
        filename  = 'produkty-wszystkie/produkty-wszystkie.xml'
        if not os.path.exists(filename):
            print DUPA
            exit(-1)
        
        root = et.parse(filename).getroot()
        for base in root[:2]:
            for book in base[:3]:
                book_dict = self.make_dict(book)
                print book_dict
#            print "Tytul: ",book_dict['title']
#            print "ID: ", book_dict['id']
#            print "Opis: ", book_dict['description']
#            print "url: ",book_dict['url']
#            print 

   
