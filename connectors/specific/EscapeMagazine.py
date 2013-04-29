from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *
import os

class EscapeMagazine(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './producer_ident':('isbn',''),
        './id':('external_id',''),
        './title':('title',''),
        './describe_long':('description',''),
        './describe_short':('description_short',''),
        './status':('status', 0),
        './price':('price', 0),
        './price_promo':('price_promotion', 0),
        "./*[contains(name(), 'authors_')]":('authors',''),
        "./*[contains(name(), 'categories_')]":('categories',''),
        "./*[contains(name(), 'covers_')]":('cover',''),
        './title_sub':('subtitle', ''),
        './producer_producer':('publisher', ''),
        './url':('url', ''),
    }

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, price_tag_name="price_promotion")
        self.validate_flat_list(dic, "categories")
        super(EscapeMagazine, self).validate(dic)

    def validate_flat_list(self, dic, tag_name):
        if dic.get(tag_name) != None:
            if isinstance(dic.get(tag_name), list):
                tag=unicode(dic[tag_name][0]) if len(dic[tag_name]) > 0 else u""
                for elem in dic[tag_name][1:]:
                    tag = tag + u", " + unicode(elem)
                dic[tag_name] = tag

Base = SqlWrapper.getBaseClass()
class EscapeMagazineBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    isbn= Column(Unicode(13))               #13
    external_id = Column(Integer)           #6
    title = Column(Unicode(128))            #68
    #description
    status = Column(Integer)                #1
    price = Column(Integer)                 #grosze
    price_promotion = Column(Integer)       #grosze
    #authors
    categories = Column(Unicode(32))        #18
    cover = Column(Unicode(128))            #108
    subtitle = Column(Unicode(128))         #0
    publisher = Column(Unicode(32))         #15
    url = Column(Unicode(128))              #94

class EscapeMagazineBookDescription(GenericBookDescription, Base):
    pass

class EscapeMagazineAuthor(GenericAuthor, Base):
    pass

class EscapeMagazineBookPrice(GenericBookPrice, Base):
    pass

class EscapeMagazineBooksAuthors(GenericBooksAuthors, Base):
    pass

