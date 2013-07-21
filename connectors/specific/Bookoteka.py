from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Bookoteka(XMLConnector):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'title':('./title', ''),
        'formats':('./format', ''),
        'price':('./price', ''),
        'isbns':('./isbn', ''),
        'cover':('./coverUrl', ''),
        'url':('./url', ''),
        'authors': ("./*[contains(name(), 'author_')]", ''),
    }

    uni_dict = {}

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)
        self.merge_duplicates(dic)

    def create_id_from_url(self, dic):
        dic['external_id'] = dic['url'].split('/')[-1]

    def merge_duplicates(self, dic):
        existing = self.uni_dict.get(dic['external_id'])
        if existing == None:
            self.uni_dict[dic['external_id']] = dic
        elif existing != dic:
            for key in dic.keys():
                if existing.get(key) == None:
                    existing[key] = dic[key]
                elif existing[key] != dic[key]:
                    #is list
                    if isinstance(existing[key], list) and not isinstance(existing[key], basestring):
                        existing[key].append(dic[key])
                    else:
                        existing[key] = [existing[key], dic[key]]

    def validate(self, dic):  pass
    def add_record(self, dic):  pass

    def validateISBNs(self, dic, id, title):
        if "," in dic["isbns"]:
            dic["isbns"] = [x.strip().split(" ")[0] for x in dic["isbns"].split(",")]

        super(Bookoteka, self).validateISBNs(dic, id, title)


    def after_parse(self):
        for dic in self.uni_dict.values():
            super(Bookoteka, self).validate(dic)
            #self.measureLenghtDict(dic)
            super(Bookoteka, self).add_record(dic)


Base = SqlWrapper.getBaseClass()

class BookotekaBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    external_id = Column(Unicode(64), unique = True)    #10

    title = Column(Unicode(265))                        #131
    url = Column(Unicode(128))                          #107
    #authors
    format = Column(Unicode(8))                         #4
    cover = Column(Unicode(256))                        #139
    price = Column(Integer)                             #grosze
    isbn = Column(Unicode(13))                          #0

