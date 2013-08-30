from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class ZielonaSowa(Afiliant):
    xml_tag_dict = dict (Afiliant.xml_tag_dict.items() + [('authors', ("./n:attributes/n:attribute[n:name='Producent']/n:value", ''))])

class ZielonaSowaBook(GenericBook, Base):
    category = Column(Unicode(32))      #18
    #title(256)                         #71
    #price = Column(Integer)       
    url = Column(Unicode(128))           #60
    #cover = Column(Unicode(256))        #114

