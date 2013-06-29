from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Empik(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './isbn':('isbns', ''),                   #ok
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
    id = Column(Integer, primary_key = True)
    ean = Column(Unicode(13))           #13
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(65))           #59
    cover = Column(Unicode(280))        #269
    availability = Column(Unicode(10))  #0

