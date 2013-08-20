from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    xml_tag_dict = dict (Afiliant.xml_tag_dict.items() + [('publisher', (u"./n:attributes/n:attribute[n:name='Producent']/n:value", ''))])

class TmcBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id = Column(Integer, unique=True)
    #title
    #price
    #price_normal
    url = Column(Unicode(128))           #60
    cover = Column(Unicode(64))         #52
    category = Column(Unicode(128))      #82
    publisher = Column(Unicode(128))     #73

