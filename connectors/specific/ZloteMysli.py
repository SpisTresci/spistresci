from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class ZloteMysli(Afiliant):

    xml_attributes_dict = {
        'Autor':('authors', ''),
        'ISBN':('isbn', ''),
        'Wydawnictwo':('publisher', ''),
        'Rok wydania':('date', ''),
        'Format':('object_format', ''),
        'Format pliku':('format', ''),
        u'Ilo\u015b\u0107 stron':('length', ''),
        'Oprawa':('binding', ''),
        #it may be sth different than image tag
        'zm:imageParent':('cover_zm', ''),
        'zm:imageMedium':('cover_medium', ''),
        'zm:imageSmall':('cover_small', ''),
        #it may be sth different than category
        'zm:categoryId':('category_id', ''),
        'zm:productTypeId':('product_type_id', ''),
    }

class ZloteMysliBook(GenericBook, Base):

    #external_id
    category = Column(Unicode(21))      #21
    categoryId = Column(Integer)        #2
    publisher = Column(Unicode(22))     #22
    format = Column(Unicode(13))        #13
    isbn = Column(Unicode(13))          #13
    #price
    binding = Column(Unicode(6))        #6
    date = Column(Unicode(4))           #4    #TODO: change to Date
    #title
    url = Column(Unicode(165))          #165
    cover = Column(Unicode(70))         #70
    cover_zm = Column(Unicode(70))      #70    #TODO: what is it zm?
    cover_small = Column(Unicode(70))   #69
    cover_medium = Column(Unicode(70))  #70
    product_type_id = Column(Integer)
    object_format = Column(Unicode(2))  #2
    length = Column(Unicode(25))        #25
