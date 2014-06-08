from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Wydaje(XMLConnector):

    depth = 1

    inner_offer_dict = {
        'formats': ('./formats/format', ''),
        'price': ('./price', '')
    }

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', ''),
        'title': ('./title', ''),
        'authors': ('./authors/author/name', ''),
        'isbns': ('./isbn', ''),
        'pages': ('./pages', ''),
        'tags': ('./tags', ''),
        'categories': ('./categories/category', ''),
        'url': ('./url', ''),
        'cover': ('./cover', ''),
        'sample': ('./sample', ''),
        'rating': ('./rating', ''),
        'votes': ('./votes', ''),
        'description': ('./description', ''),
        'offers': ("./offers/offer" + str(inner_offer_dict), ''),
    }

    format_convert_dict = {
        'book':'ks'
    }


    def validate(self, dic):
        self.validateRating(dic)
        super(Wydaje, self).validate(dic)

    def validatePrice(self, dic, id, title, price_tag_name = 'price', default_price=0):
        pass

    def validateRating(self, dic):
        if dic.get('rating'):
            dic['rating'] = int(round(float(dic['rating'])/6, 3) * 100)

    def parse(self, force=False):
        self.save_time_of_("parse_start")
        self.before_parse()
        book_number = 0

        if force or self.areDataDifferentThanPrevious():
            for filename in self.fetched_files:
                for offer in self.getBookList(filename):
                    book_number += 1
                    if book_number < self.skip_offers + 1:
                        continue
                    elif self.limit_books and book_number > self.limit_books:
                        break

                    book = self.makeDict(offer)

                    if not isinstance(book['offers'], list):
                        book['offers'] = [book['offers']]

                    book_template = book
                    i = 0
                    for offer in book['offers']:
                        book = dict(book_template)
                        book['external_id'] += '-'+str(i)
                        for key in self.inner_offer_dict.keys():
                            book[key] = offer[key]

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


class WydajeBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    external_id = Column(Unicode(10), unique=True)
    title = Column(Unicode(256))        #140
    #authors
    #isbns
    pages = Column(Integer)
    tags = Column(Unicode(256))          #250
    #categories - #TODO
    #url
    #cover
    sample = Column(STUrl)        #170
    rating = Column(Integer)
    votes = Column(Integer)
    #description
    #price
    #price_normal
    #formats
