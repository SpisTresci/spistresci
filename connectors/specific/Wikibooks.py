from connectors.generic import XMLConnector
import lxml.etree as et
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()
class Wikibooks(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':("@id", ''),
        'url':("./a/@href", ''),
        'title':("./a/@title", ''),
        'cover':("./a/@cover", ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("//div[@id='mw-pages']/div[@lang='pl' and @dir='ltr' and @class='mw-content-ltr']/table/tr/td/ul")

    #Wikibooks does not allow download wikipages without defined user-agent
    def downloadFile(self, url = None, filename = None, headers = None):
        super(Wikibooks, self).downloadFile(url, headers = {'User-Agent':'Mozilla/5.0'})


    #TODO: use generic PARSE 
    def parse(self):
        self.before_parse()
        book_number = 0
        for filename in self.fetched_files:
            root = et.parse(filename).getroot()
            ULs = list(self.weHaveToGoDeeper(root, self.depth))
            for ul in ULs:
                for li in ul:
                    book_number += 1
                    if book_number < self.skip_offers + 1:
                        continue
                    elif self.limit_books and book_number > self.limit_books:
                        break
                    dic = self.makeDict(li)
                    #comment out when creating connector
                    self.adjust_parse(dic)
                    self.validate(dic)
                    #uncomment when creating connector
                    #self.measureLenghtDict(dic)
                    #print dic
                    #comment out when creating connector
                    self.add_record(dic)

        self.after_parse()
        #uncomment when creating connector
        #print self.max_len


    def adjust_parse(self, dic):
        if dic.get("url"):
            dic["url"] = "http://pl.wikibooks.org/wiki/" + dic["url"].split("/")[-1]
            dic["external_id"] = dic["url"]
        if dic.get("title"):
            dic["title"] = dic["title"].split("/")[-1]

        dic['publisher'] = dic['authors'] = "Wikibooks"
        dic['formats'] = ['pdf', 'epub', 'odf', 'online']

class WikibooksBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    external_id = Column(Unicode(128))
    publisher = Column(Unicode(16))
    title = Column(Unicode(64), unique = True)
    #url
    #cover
    price = Column(Integer)
