from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Zantes(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', ''),
        'date': ('./time', ''),
        'title': ('./title', ''),
        'isbns': ('./producer_ident', ''),
        'description_short': ('./describe_short', ''),
        'description': ('./describe_long', ''),
        'status': ('./status', 0),
        'price': ('./price', 0),
        'price_promotion': ('./price_promo', 0),
        'authors': ("./*[contains(name(), 'authors_')]", ''),
        'cover': ("./*[contains(name(), 'covers_')]", ''),
        'subtitle': ('./title_sub', ''),
        'categories': ("./*[contains(name(), 'categories_')]", ''),
        'publisher_id': ('./producer_id', ''),
        'publisher': ('./producer_producer', ''),
        'url': ('./url', ''),
    }

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, price_tag_name = "price_promotion")
        self.validate_flat_list(dic, "categories")
        super(Zantes, self).validate(dic)

    def validate_flat_list(self, dic, tag_name):
        if dic.get(tag_name) != None:
            if isinstance(dic.get(tag_name), list):
                tag = unicode(dic[tag_name][0]) if len(dic[tag_name]) > 0 else u""
                for elem in dic[tag_name][1:]:
                    tag = tag + u", " + unicode(elem)
                dic[tag_name] = tag

    def adjust_parse(self, dic):
        dic['formats'] = ['mp3']

Base = SqlWrapper.getBaseClass()

class ZantesBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    date = Column(DateTime)
    title = Column(Unicode(128))            #91
    #description
    #description_short - not taken
    status = Column(Integer)                #1
    price = Column(Integer)                 #grosze
    price_promotion = Column(Integer)       #grosze
    #authors
    cover = Column(Unicode(128))            #180
    subtitle = Column(Unicode(128))         #0
    categories = Column(Unicode(256))       #141
    publisher_id = Column(Integer)          #15
    publisher = Column(Unicode(64))         #35
    url = Column(Unicode(128))              #98
