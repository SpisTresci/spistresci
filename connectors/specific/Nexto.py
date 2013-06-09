from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Nexto(XMLConnector):
    #dict of xml_tag -> db_column_name translations

    inner_offer_dict = {
        'date':('./publication-date', ''),
        'activation_date':('./activation-date', ''),
        'price_normal':('./price/price-original', ''),
        'price_for_not_registered':('./price/price-normal', ''),
        'price':('./price/price-club', ''),
        'formats':('./formats-all', ''),
        'cover':('./covers/cover', ''),
        'authors':('./authors/author', ''),
        'lectors':('./lectors/lector', ''),
        'audio_time':('./audiobook-length', ''),
        'page_count':('./pages-count', ''),
        'free_fragment':('./free-fragments/free-fragment', ''),
        'tocs':('./tocs/table-of-content', ''),
    }

    xml_tag_dict = {
        'external_id':('@product-id',''),
        'title':('./name', ''),
        'type':('./type', ''),
        'url':('./url',''),
        'categories':('./category', None),
        'isbns':('./issn', ''),
        'publisher':('./manufacturer', ''),
        'lang':('./language', ''),
        'description':('./description', ''),
        'rating':('./review-note', ''),
        'offers':('./issues/issue' + str(inner_offer_dict), None),
    }

    format_convert_dict = dict(XMLConnector.format_convert_dict.items() + {
        '\(znak wodny\)':'',
    }.items())

    format_sepeparators = [',']

    def downloadFile(self, url=None, filename=None, headers=None):
        super(Nexto, self).downloadFile(url=url, filename=filename, headers={'accept-encoding':'gzip'})

    def parse(self):
        self.save_time_of_("parse_start")
        self.before_parse()
        book_number = 0
        if self.areDataDifferentThanPrevious():
            for filename in self.fetched_files:
                for offer in self.getBookList(filename):
                    book_number += 1
                    if book_number < self.skip_offers + 1:
                        continue
                    elif self.limit_books and book_number > self.limit_books:
                        break

                    book = self.makeDict(offer)

                    default_inner_offer = not book['offers']
                    offers = book['offers'] if isinstance(book['offers'], list) else [book['offers']]

                    del book['offers']
                    book_template = book
                    i = 0
                    for offer in offers:
                        book = dict(book_template)
                        book['external_id'] += '-'+str(i)
                        for key in self.inner_offer_dict.keys():
                            book[key] = offer[key] if not default_inner_offer else self.inner_offer_dict[key][1]

                        self.adjust_parse(book)
                        self.validate(book)
                        if self.fulfillRequirements(book):
                            #uncomment when creating connector
                            #self.measureLenghtDict(book)
                            #comment out when creating connector
                            self.add_record(book)
                        i+=1

            self.after_parse()
            #uncomment when creating connector
            #print self.max_len
            #print self.max_len_entry
            self.session.commit()
            self.save_info_about_offers(offers_parsed = book_number)
        else:
            self.save_info_about_offers(offers_new = 0)

        self.save_time_of_("parse_end")

    def validate(self, dic):
        self.validateRating(dic)
        super(Nexto, self).validate(dic)

    def validateRating(self, dic):
        if dic.get('rating'):
            dic['rating'] = int(round(float(dic['rating'])/5, 2) * 100)

    def adjust_parse(self, dic):

        for key in ['cover', 'free_fragment']:
            if not isinstance(dic[key], basestring) and isinstance(dic[key], list):
                dic[key] = dic[key][0]


Base = SqlWrapper.getBaseClass()

class NextoBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    external_id = Column(Unicode(10), unique=True)
    title = Column(Unicode(512))            #293
    url = Column(Unicode(512))              #331
    #categories #TODO
    #isbns
    publisher = Column(Unicode(128))        #69
    lang = Column(Unicode(4))               #2
    #description
    rating = Column(Integer)

    date = Column(Unicode(16))              #10
    activation_date = Column(Unicode(16))   #10
    #price
    #price_normal
    #formats
    cover = Column(Unicode(512))            #280
    #authors
    #lectors
    audio_time = Column(Unicode(32))        #28
    page_count = Column(Unicode(64))        #33
    free_fragment = Column(Unicode(512))    #290
    #tocs
