from connectors.common import Afiliant
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class ZielonaSowa(Afiliant):
    xml_tag_dict = dict (Afiliant.xml_tag_dict.items() + [('authors', ("./n:attributes/n:attribute[n:name='Producent']/n:value", ''))])

    def adjust_parse(self, dic):
        #all ZielonaSowa ebooks are pdf, audiobooks - mp3
        if 'E-booki' in dic['category']:
            dic['formats'] = ['pdf']
        elif 'Audiobooki' in dic['category']:
            dic['formats'] = ['mp3']
        else:
            dic['formats'] = ['unknown']

class ZielonaSowaBook(GenericBook, Base):
    category = Column(Unicode(32))      #18
    #title(256)                         #71
    #price = Column(Integer)       
    url = Column(Unicode(128))           #60
    #cover = Column(Unicode(256))        #114

