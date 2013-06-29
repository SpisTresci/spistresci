from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Legimi(Afiliant):
    pass

class LegimiBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)

    category = Column(Unicode(90))      #82
    publisher = Column(Unicode(80))     #73
    title = Column(Unicode(165))       #155
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(60))         #52
    year = Column(Unicode(4))           #4 #TODO: correct name of collumnq
    length = Column(Unicode(20))        #16
    #lectors
    format = Column(Unicode(25))        #23 #TODO: store format in proper way

