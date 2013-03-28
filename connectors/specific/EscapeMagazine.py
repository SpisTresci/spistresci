from connectors.generic import XMLConnector
from xml.etree import ElementTree as et
import os

class EscapeMagazine(XMLConnector):
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        'producer_ident':'isbn',
        'id':'id',
        'title':'title',
        'describe_long':'description',
        'describe_short':'description',
        'status':'status',
        'price':'price',
        'price_promo':'discount',
        #tag suggests that there might be more than one cover,
        #however currently we do not support that
        'covers_0':'cover',

        #we don't need to add these here 
        #since it's done later in add_list method
        #'authors_0':'author',
        #'categories_0':'category',

        #whatever it is
        'title_sub':'title_sub',
        'producer_producer':'publisher',
        'url':'url',
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


    def add_list(self,book,book_dict,key,xml_tag_prefix):
        num = 0
        new_item = book.findtext('%s_%d'%(xml_tag_prefix,num))
        book_dict[key] = []
        while new_item:
            book_dict[key].append(new_item)
            num+=1
            new_item = book.findtext('%s_%d'%(xml_tag_prefix,num))

    def make_dict(self,book):
        book_dict = XMLConnector.make_dict(self,book) 
        self.add_list(book,book_dict,'author','authors')
        self.add_list(book,book_dict,'category','categories')

        #actually we don't want a list of covers, just first one
#        self.add_list(book,book_dict,'cover','covers')
        return book_dict
        
        #add authors



        #add categories


   
