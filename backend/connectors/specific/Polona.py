from connectors.generic import OAIConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Polona(OAIConnector):

    format_convert_dict = dict(OAIConnector.format_convert_dict.items() + {
        'image/text':'online',
    }.items())

    #dict of xml_tag -> db_column_name translations
    translate_tag_dict = {
        'title':('title', ''),
        'lang':('language', ''),
        'publisher':('publisher', ''),
        'formats':('format', ''),
        'authors':('creator', ''),
        'contributors':('contributor', ''),
        'url':('identifier', ''),
        'type':('type', ''),
        'date':('date', ''),
        'rights':('rights', ''),
        'subjects':('subject', ''),
        'relations':('relation', ''),
        'description':('description', ''),
        'source':('source', ''),
        'coverage':('coverage',''),
    }

    def adjust_parse(self, dic):
        for key in self.translate_tag_dict.keys():
            if dic.get(key) and not isinstance(dic[key], basestring):
                dic[key] = ', '.join(dic[key])

        dic['is_available'] = 'domena publiczna' in dic['rights'].lower()
        dic['external_id'] = int(dic['url'].split('/')[4])
        dic['formats'] = ['online']


Base = SqlWrapper.getBaseClass()

class PolonaBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    #external_id
    title = Column(Unicode(1024))           #835
    lang = Column(Unicode(64))              #7*5
    publisher = Column(Unicode(256))        #232
    #formats
    #authors
    contributors = Column(Unicode(1024))     #
    #url
    type = Column(Unicode(32))              #24
    date = Column(Unicode(128))             #67
    rights = Column(Unicode(512))           #451
    subjects = Column(Unicode(2048))        #1604
    relations = Column(Unicode(512))        #
    #description
    source = Column(Unicode(64))            #39
    coverage = Column(Unicode(128))         #
    is_available = Column(Boolean)
