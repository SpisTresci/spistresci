from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class EscapeMagazine(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'isbns': ('./producer_ident', ''),
        'external_id': ('./id', ''),
        'title': ('./title', ''),
        'description': ('./describe_long', ''),
        'description_short': ('./describe_short', ''),
        'status': ('./status', 0),
        'price': ('./price', 0),
        'price_promotion': ('./price_promo', 0),
        'authors': ("./*[contains(name(), 'authors_')]", ''),
        'categories': ("./*[contains(name(), 'categories_')]", ''),
        'cover': ("./*[contains(name(), 'covers_')]", ''),
        'subtitle': ('./title_sub', ''),
        'publisher': ('./producer_producer', ''),
        'url': ('./url', ''),
    }

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, price_tag_name = "price_promotion")
        self.validate_flat_list(dic, "categories")
        super(EscapeMagazine, self).validate(dic)

    def validate_flat_list(self, dic, tag_name):
        if dic.get(tag_name) != None:
            if isinstance(dic.get(tag_name), list):
                tag = unicode(dic[tag_name][0]) if len(dic[tag_name]) > 0 else u""
                for elem in dic[tag_name][1:]:
                    tag = tag + u", " + unicode(elem)
                dic[tag_name] = tag

    def adjust_parse(self, dic):
        dic['formats'] = 'pdf'

Base = SqlWrapper.getBaseClass()

class EscapeMagazineBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
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
