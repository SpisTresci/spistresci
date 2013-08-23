# vim: set fileencoding=utf-8
from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class ZloteMysli(Afiliant):
    #TODO: testy
    xml_tag_dict = dict(Afiliant.xml_tag_dict.items() + [
        ('authors', ("./n:attributes/n:attribute[n:name='Autor']/value", '')),
        ('isbns', ("./n:attributes/n:attribute[n:name='ISBN']/n:value", '')),
        ('publisher', ("./n:attributes/n:attribute[n:name='Wydawnictwo']/n:value", '')),
        ('formats', ("./n:attributes/n:attribute[n:name='Format pliku']/n:value", '')),
        ('date', ("./n:attributes/n:attribute[n:name='Rok_wydania']/n:value", '')),
        #('object_format', ("./n:attributes/n:attribute[n:name='Format']/n:value", '')),
        ('length', (u"./n:attributes/n:attribute[n:name='Ilość stron']/n:value", '')),
        #('binding', ("./n:attributes/n:attribute[n:name='Oprawa']/n:value", '')),
        ('cover_parent', ("./n:attributes/n:attribute[n:name='zm:imageParent']/n:value", '')),
        ('cover_medium', ("./n:attributes/n:attribute[n:name='zm:imageMedium']/n:value", '')),
        ('cover_small', ("./n:attributes/n:attribute[n:name='zm:imageSmall']/n:value", '')),
        #According to http://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #the last value under key 'category' will be set to dict
        ('category', ("./n:attributes/n:attribute[n:name='zm:categoryId']/n:value", '')),
        ('product_type_id', ("./n:attributes/n:attribute[n:name='zm:productTypeId']/n:value", '')),
    ])


class ZloteMysliBook(GenericBook, Base):

    #external_id
    category = Column(Unicode(21))      #21
    categoryId = Column(Integer)        #2
    publisher = Column(Unicode(22))     #22
    isbn = Column(Unicode(13))          #13
    #price
    date = Column(Unicode(4))           #4   
    #title
    url = Column(Unicode(165))          #165
    cover = Column(Unicode(70))         #70
    cover_parent = Column(Unicode(70))  #70    #TODO: what is it zm?
    cover_small = Column(Unicode(70))   #69
    cover_medium = Column(Unicode(70))  #70
    product_type_id = Column(Integer)
    length = Column(Unicode(25))        #25
