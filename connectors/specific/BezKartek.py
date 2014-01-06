from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class BezKartek(XMLConnector):

    depth = 1
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'isbns': ('./isbn', ''),
        'external_id': ('./ebookId', None),
        'title': ('./name', ''),
        'url': ('./url', None),
        'authors': ('./authors', ''),
        'category': ('./category', ''),
        'description': ('./description', ''),
        'formats': ('./format', ''),
        'cover': ('./image', ''),
        'lang_short': ('./languages/lang_short', ''),
        'lang_long': ('./languages/lang_long', ''),
        'price': ('./price', 0),
        'page_count': ('./pageCount', 0),
        'publisher': ('./publisher', ''),
        'security': ('./securityType', ''),
        'audio_time': ('./audioTime', ''),
    }
    
    #T480 price already in gr
    def validatePrice(self, dic, id, title, price_tag_name = 'price', default_price=0):
        price = dic.get(price_tag_name, default_price)
        try:
            int(price)
        except ValueError:
            self.erratum_logger.warning("Entry has price in wrong format! connector: %s, id: %s, title: %s, price: %s" % (self.name, id, title, str(price)))
            price = default_price
        finally:
             dic[price_tag_name] = unicode(price)

Base = SqlWrapper.getBaseClass()

class BezKartekBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    category = Column(Unicode(30))      #29

    audio_time= Column(Unicode(16))    #9
    #price = Column(Integer)             #GROSZE!!!
    page_count = Column(Unicode(16))        #508700 - wtf?
    publisher = Column(Unicode(128))     #68
    url = Column(Unicode(512))          #265
    #cover = Column(Unicode(256))        #184
    security = Column(Unicode(16))      #9
    lang_short = Column(Unicode(2))     #2
    lang_long = Column(Unicode(16))     #9
