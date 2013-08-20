from connectors.common import FormatInTitleConnector
from sqlwrapper import *
from connectors.generic import GenericBook
import re

Base = SqlWrapper.getBaseClass()

class Audiobook(FormatInTitleConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('./id', ''),
        'price':('./price', 0),
        'url':('./url', ''),
        'category':('./category', ''),
        'title':('./name', ''),
        'raw_title':('./name', ''),
        'description':('./description', ''),
        'publisher':("./attribute[@name='wydawnictwo']", ''),
        'authors':("./attribute[@name='autor']", ''),
        'length':("./attribute[@name='czas']", 0),
    }

    def adjust_parse(self, dic):
        authors = dic.get('authors', '')
        title = dic.get('title', '')
        if authors in title:
            title = title.replace(authors, '')
            dic['title'] =re.sub('^ *, *', '', title)
        super(Audiobook, self).adjust_parse(dic)
        #FIXME: there is no cover info in xml, hardcoded for now - T370
        dic['cover'] = ''
        

class AudiobookBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id
    #title = Column(Unicode(256))       #168
    raw_title = Column(Unicode(256))    #168
    #price = Column(Integer)
    #price_normal
    url = Column(Unicode(512))          #294
    #there is no cover info
#    cover = Column(Unicode(128))        #118
    category = Column(Unicode(128))      #63
    length = Column(Integer)
    publisher = Column(Unicode(64))     #49

