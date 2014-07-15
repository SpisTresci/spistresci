# vim: set fileencoding=utf-8
from connectors.common import Afiliant, FormatInTitleConnector
from sqlwrapper import *
from connectors.generic import GenericBook
import utils


Base = SqlWrapper.getBaseClass()

class ZloteMysli(Afiliant, FormatInTitleConnector):
    xml_tag_dict = dict(Afiliant.xml_tag_dict.items() + [
        ('raw_title', ('./n:name', '')),
        ('authors', ("./n:attributes/n:attribute[n:name='Autor']/n:value", '')),
        ('isbns', ("./n:attributes/n:attribute[n:name='ISBN']/n:value", '')),
        ('publisher', ("./n:attributes/n:attribute[n:name='Wydawnictwo']/n:value", '')),
        ('formats', ("./n:attributes/n:attribute[n:name='Format pliku']/n:value", '')),
        ('date', ("./n:attributes/n:attribute[n:name='Rok wydania']/n:value", '')),
        #('object_format', ("./n:attributes/n:attribute[n:name='Format']/n:value", '')),
        ('page_count', (u"./n:attributes/n:attribute[n:name='Ilość stron']/n:value", '')),
        #('binding', ("./n:attributes/n:attribute[n:name='Oprawa']/n:value", '')),
        ('cover_parent', ("./n:attributes/n:attribute[n:name='zm:imageParent']/n:value", '')),
        ('cover_medium', ("./n:attributes/n:attribute[n:name='zm:imageMedium']/n:value", '')),
        ('cover_small', ("./n:attributes/n:attribute[n:name='zm:imageSmall']/n:value", '')),
        #According to http://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #the last value under key 'category' will be set to dict
        ('category', ("./n:attributes/n:attribute[n:name='zm:categoryId']/n:value", '')),
        ('product_type_id', ("./n:attributes/n:attribute[n:name='zm:productTypeId']/n:value", '')),
        ('availability', ('./n:availability','')),
    ])

    def adjust_parse(self, dic):
        super(ZloteMysli, self).adjust_parse(dic)
        #convert category to list
        dic['category'] = utils.Str.listToUnicode(dic.get('category'))


class ZloteMysliBook(GenericBook, Base):
    #id
    #external_id
    #title
    raw_title = Column(Unicode(256))    #126
    category = Column(Unicode(32))      #6
    publisher = Column(Unicode(32))     #22
    #price
    date = Column(Unicode(4))           #4
    #url
    #cover
    cover_parent = Column(STUrl)  #70
    cover_small = Column(STUrl)   #69
    cover_medium = Column(STUrl)  #70
    product_type_id = Column(Integer)
    page_count = Column(Unicode(25))        #32
