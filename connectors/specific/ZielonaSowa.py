from connectors.common import Afiliant
from connectors.generic import GenericBook
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class ZielonaSowa(Afiliant):
    pass

class ZielonaSowaBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

    category = Column(Unicode(90))      #82
    #title(255)                         #82
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(120))        #115
    #lectors
    manufacturer = Column(Unicode(70)) #63
