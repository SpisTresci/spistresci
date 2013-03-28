import os
from connectors.generic import *
from xml.etree import ElementTree as et
from sqlwrapper import *

class Empik(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        #'isbn':('isbn', ''),                   #ok
        'ean':('ean', ''),                      #ok
        'TDProductId':('external_id', None),    #ok
        'name':('title', ''),                   #ok
        'productUrl':('url', None),             #ok
        'imageUrl':('cover', None),             #ok
        'description':('description', ''),
        'price':('price', 0),                   #ok
        #'availability':('availability',''),    #ok
    }


    def parse(self):
        filename = os.path.join(self.unpack_dir, self.unpack_file)
        products = list(et.parse(filename).getroot())
        if self.limit_books:
            products = products[:self.limit_books]
        for book in products:
            dic = self.make_dict(book)
            self.validate(dic)
            #self.measureLenghtDict(dic)
            self.add_record(dic)

        #print self.max_len
        #for key in self.max_len_entry.keys():
        #    print key+": "+ unicode(self.max_len_entry[key])


Base = SqlWrapper.getBaseClass()

class EmpikBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    ean = Column(Unicode(13))           #13
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(65))           #59
    cover = Column(Unicode(280))        #269

class EmpikBookDescription(GenericBookDescription, Base):
    pass

class EmpikAuthor(GenericAuthor, Base):
    pass

class EmpikBookPrice(GenericBookPrice, Base):
    pass

class EmpikBooksAuthors(GenericBooksAuthors, Base):
    pass
