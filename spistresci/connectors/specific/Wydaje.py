from decimal import Decimal

from spistresci.connectors.generic import XMLConnector

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

    def validatePrice(self, dic, id, title, price_tag_name = 'price', default_price='0.00'):

        original_price = dic.get(price_tag_name, default_price)
        if original_price != default_price and original_price != '':
            dic[price_tag_name] = Decimal(dic[price_tag_name])/100
        else:
            dic[price_tag_name] = Decimal(default_price)


    def validateRating(self, dic):
        if dic.get('rating'):
            dic['rating'] = int(round(float(dic['rating'])/6, 3) * 100)

    # def parse(self, force=False):
    #     self.save_time_of_("parse_start")
    #     self.before_parse()
    #     book_number = 0
    #
    #     if force or self.areDataDifferentThanPrevious():
    #         for filename in self.fetched_files:
    #             for offer in self.getBookList(filename):
    #                 book_number += 1
    #                 if book_number < self.skip_offers + 1:
    #                     continue
    #                 elif self.limit_books and book_number > self.limit_books:
    #                     break
    #
    #                 book = self.makeDict(offer)
    #
    #                 if not isinstance(book['offers'], list):
    #                     book['offers'] = [book['offers']]
    #
    #                 book_template = book
    #                 i = 0
    #                 for offer in book['offers']:
    #                     book = dict(book_template)
    #                     book['external_id'] += '-'+str(i)
    #                     for key in self.inner_offer_dict.keys():
    #                         book[key] = offer[key]
    #
    #                     self.adjust_parse(book)
    #                     self.validate(book)
    #                     if self.fulfillRequirements(book):
    #                         #uncomment when creating connector
    #                         #self.measureLenghtDict(book)
    #                         #comment out when creating connector
    #                         self.add_record(book)
    #                     i+=1
    #
    #         self.after_parse()
    #         #uncomment when creating connector
    #         #print self.max_len
    #         #print self.max_len_entry
    #         self.session.commit()
    #         self.save_info_about_offers(offers_parsed = book_number)
    #     else:
    #         self.save_info_about_offers(offers_new = 0)
    #
    #     self.save_time_of_("parse_end")

    def parse(self, force=False):
        self.before_parse()
        book_number = 0
        force = True # TODO - REMOVE ASAP
        if self.areDataDifferentThanPrevious() or force:
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
                        book['external_id'] += str(i)
                        for key in self.inner_offer_dict.keys():
                            book[key] = offer[key]

                        self.adjust_parse(book)
                        self.validate(book)
                        if self.fulfillRequirements(book):
                            self.create_pp_url(book)
                            self.new_add_record(book)
                        i+=1


                    self.bookstore_cmd_status.feed_dog()

            self.after_parse()
