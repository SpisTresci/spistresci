from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook
import utils

class Publio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('./id', ''),
        'title':('./title', ''),
        'authors':('./authors', ''),
        'formats':('./formats', ''),
        'protection':('./protectionType', ''),  #???
        'price':('./price', ''),
        'url':('./productUrl', ''),
        'cover':('./imageUrl', ''),
        'isbns':('./isbns', ''),
        'publisher':('./company', ''),
        'category':('./categories/category', ''),
    }

    def adjust_parse(self, dic):
        #convert category to list
        dic['category'] = utils.Str.listToUnicode(dic.get('category'))

Base = SqlWrapper.getBaseClass()

class PublioBook(GenericBook, Base):
    #external_id
    title = Column(Unicode(256))
    #authors
    #formats
    #price
    #url
    #cover
    #isbns
    publisher = Column(Unicode(128))
    category = Column(Unicode(256))
    #protection - TODO T331
    #categories - TODO T334
