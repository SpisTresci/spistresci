from connectors.common import Afiliant
from connectors.generic import GenericBook
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Audiobook(Afiliant):
    pass

class AudiobookBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)

    category = Column(Unicode(25))      #21
    #title(255)                         #122
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(1))         #0
