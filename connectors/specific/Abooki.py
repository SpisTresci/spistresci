from connectors.common import Ceneo
from sqlwrapper import *
from connectors.generic import GenericBook
import re

Base = SqlWrapper.getBaseClass()

class Abooki(Ceneo):
    depth = 0

    def __init__(self, name = None, limit_books = 0):
        super(Abooki, self).__init__(name, limit_books)
        self.supported_formats = sorted(self.supported_formats, cmp = lambda x, y: cmp(len(x), len(y)), reverse = True)
        self.accepted_suffix_patterns = self.config.get('accepted_suffix_patterns', '')

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':("./attrs/a[@name='ShopProductId']", ''),
        'afiliant_id':('@id', ''),
        'price':('@price', 0),
        'url':('@url', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        #this is to show user orginal (raw) title, cause we are changing it later
        'raw_title':('./name', ''),
        'cover':("./imgs/main[@url]", ''),
        'description':('./desc', ''),
        'authors':("./attrs/a[@name='Producent']", ''),
    }

    def adjust_parse(self, dic):
        title = dic['title']
        splited = re.split('!|\?|,|\.', dic['title'])
        if len(splited) > 1:
            format_string = splited[-1].strip()
        else:
            format_string = ''
            dic['formats'] = format_string
            return

        lowered_format = format_string.lower()
        if any(sf in lowered_format for sf in self.supported_formats):
            dic['formats'] = unicode(lowered_format)
            title = title.replace(format_string, '')
            dic['title'] =re.sub(' *, *$','',title)
            
        else:
            dic['formats'] = ''

    '''Note: This is dirty hack, but this is because Abooki xml is broken'''
    def _clear_suffixes_from_config(self, suffix):
        for x in self.accepted_suffix_patterns.split(','):
            suffix = re.sub(x, '', suffix)
        return suffix

    def validateFormats(self, dic, id, title):
        format_string = dic.get('formats')
        org_format_string = format_string
        format_list = []
        for sf in self.supported_formats:
            if sf in format_string:
                format_list.append(sf)
                format_string = format_string.replace(sf, '')
        cleared_format_string = ''
        dic['formats'] = format_list
        if format_string:
            format_string = self._clear_suffixes_from_config(format_string)
        if format_string:
            self.erratum_logger.warning("Unsupported format! connector: %s, id: %s, title: %s, format: %s" % (self.name, id, title, org_format_string))
            self.erratum_logger.debug("Unsupported format!. connector %s, id: %s, tile %s, format string left is: %s" % (self.name, id, title, format_string))


class AbookiBook(GenericBook, Base):
    #id = Column(Integer, primary_key = True)
    #external_id
    afiliant_id = Column(Integer)
    #title
    #price
    #price_normal
    url = Column(Unicode(512))          #372
    category = Column(Unicode(64))      #47
    raw_title = Column(Unicode(256))    #160
    cover = Column(Unicode(128))        #79

