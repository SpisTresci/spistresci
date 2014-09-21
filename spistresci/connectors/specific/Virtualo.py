from spistresci.connectors.generic import XMLConnector


class Virtualo(XMLConnector):

    depth = 0
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'title' : ('./title', ''),
        'formats' : ('./format', ''),
        'protection': ('./security', ''),
        'price' : ('./price', 0),
        'isbns' : ('./isbn', ''),
        'cover': ('./coverId', ''),
        'authors' : ('./authors', ''),
        'url' : ('./url', ''),
        'description' : ('./description', ''),
        #not added to database
        'descriptionShort' : ('./descriptionShort', ''),
        'rating' : ('./rating', ''),
     }

    def validate(self, dic):
        super(Virtualo, self).validate(dic)
        self.validateRating(dic)

    def validateRating(self, dic, rating_tag = 'rating'):
        rating = dic.get(rating_tag, '0')
        rating_normalized = 0
        try:
            #normalize ratings 1-5 -> %
            rating_normalized = str(int(20 * float(rating.replace(',', '.'))))
        except ValueError:
            self.erratum_logger.warning('Entry has invalid rating. Connector: %s, id: %s, title: %s' % (self.name, dic.get('external_id'), dic.get('title')))
        finally:
            dic[rating_tag] = rating_normalized

    def adjust_parse(self, dic):
        self.create_id_from_url(dic)
        dic["cover"] = "http://static.virtualo.pl/media_images/normal/" + dic["cover"] + ".jpg"

    def create_id_from_url(self, dic):
        dic['external_id'] = dic['url'].split('/')[4][1:]
