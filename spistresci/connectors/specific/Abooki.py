from connectors.common import FormatInTitleConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Abooki(FormatInTitleConnector):
    depth = 0

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':("./attrs/a[@name='ShopProductId']", ''),
        'program_id':('@id', ''),
        'price':('@price', 0),
        'url':('@url', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        #this is to show user orginal (raw) title, cause we are changing it later
        'raw_title':('./name', ''),
        'cover':("./imgs/main/@url", ''),
        'description':('./desc', ''),
        'authors':("./attrs/a[@name='Producent']", ''),
    }

class AbookiBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id
    program_id = Column(Integer)
    #title
    #price
    #price_normal
    #url
    category = Column(Unicode(64))      #47
    raw_title = Column(Unicode(256))    #160
    #cover

