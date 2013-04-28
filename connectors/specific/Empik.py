import os
from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *

class Empik(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './isbn':('isbn', ''),                    #ok
        './ean':('ean', ''),                      #ok
        './TDProductId':('external_id', ''),      #ok
        './name':('title', ''),                   #ok
        './productUrl':('url', ''),               #ok
        './imageUrl':('cover', ''),               #ok
        './description':('description', ''),
        './price':('price', 0),                   #ok
        './availability':('availability', ''),    #ok
    }

Base = SqlWrapper.getBaseClass()

class EmpikBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    ean = Column(Unicode(13))           #13
    isbn = Column(Unicode(13))          #0
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(65))           #59
    cover = Column(Unicode(280))        #269
    availability = Column(Unicode(10))  #0

class EmpikBookDescription(GenericBookDescription, Base):
    pass

class EmpikAuthor(GenericAuthor, Base):
    pass

class EmpikBookPrice(GenericBookPrice, Base):
    pass

class EmpikBooksAuthors(GenericBooksAuthors, Base):
    pass
