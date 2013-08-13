from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Audioteka(Afiliant):
    xml_tag_dict = Afiliant.xml_tag_dict + {
        'authors' : ("./n:attribute[name='Autor']/value", ''),
        'publisher' : ("./n:attribute[name='wydawca']/value", ''),
        'length' : ("./n:attribute[name='Dugo\u015b\u0107']/value", ''),
    }

class AudiotekaBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    category = Column(Unicode(25))      #21
    publisher = Column(Unicode(70))     #57
    #title(255)                         #122
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(150))        #145
    length = Column(Unicode(20))        #16
    #lectors
    external_id = Column(Unicode(90), unique = True) #86    #TODO: why this id is so big?
