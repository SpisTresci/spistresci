from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook
import utils
class Empik(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    #a4b tag_dict
    #xml_tag_dict = {
    #    'isbns': ('./isbn', ''),                   #ok
    #    'ean': ('./ean', ''),                      #ok
    #    'external_id': ('./TDProductId', ''),      #ok
    #    'title': ('./name', ''),                   #ok
    #    'url': ('./productUrl', ''),               #ok
    #    'cover': ('./imageUrl', ''),               #ok
    #    'description': ('./description', ''),
    #    'price': ('./price', 0),                   #ok
    #    'availability': ('./availability', ''),    #ok
    #}

    xml_tag_dict = {
     #   'isbns': ('./isbn', ''),
        'external_id': ('@id', ''),
        'title': ('./name', ''),
        'url': ('./productURL', ''),
        'cover': ('./imageURL', ''),
        'description': ('./description', ''),
        'price': ('./price', 0),
        'authors':("./fields/field[@name='author']/@value",''),
        'formats': ("./fields/field[@name='format']/@value", ''),
        'ean': ("./fields/field[@name='ean']/@value", ''),
        'category': ('./categories/category/@name', ''),
        'availability': ('./deliveryTime', ''),
    }

    def adjust_parse(self, dic):
        #convert category to list
        dic['category'] = utils.Str.listToUnicode(dic.get('category'))

Base = SqlWrapper.getBaseClass()

class EmpikBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    #ean = Column(Unicode(13))           #13
    #price = Column(Integer)             #GROSZE!!!
    #url = Column(Unicode(65))           #59
    #cover = Column(Unicode(280))        #269
    #availability = Column(Unicode(10))  #0

    id = Column(Integer, primary_key = True)
    #title
    external_id = Column(Unicode(16), unique=True)
    ean = Column(Unicode(16))           #13
    #price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(512))           #406
    cover = Column(Unicode(512))        #269
    category = Column(Unicode(128))   #64
    availability = Column(Unicode(32))  #10

