from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class ZielonaSowa(Afiliant):
    xml_tag_dict = Afiliant.xml_tag_dict + {
        'authors' : ("./n:attribute[name='Producent']/value", ''),
    }

    #TODO: książki tylko z odpowiednim categoryId
class ZielonaSowaBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    category = Column(Unicode(90))      #82
    #title(255)                         #82
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(120))        #115
    #lectors
    manufacturer = Column(Unicode(70)) #63
