from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class Virtualo(XMLConnector):

    depth = 0
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./coverId', ''),
        'title' : ('./title', ''),
        'formats' : ('./format', ''),
        'protection': ('./security', ''),
        'price' : ('./price', 0),
        'isbns' : ('./isbn', ''),
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
        dic["cover"] = "http://static.virtualo.pl/media_images/normal/" + dic["external_id"] + ".jpg"

Base = SqlWrapper.getBaseClass()

class VirtualoBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(256))        #174
    protection = Column(Unicode(8))       #3
    price = Column(Integer)             #*0,01PLN
    url = Column(Unicode(128))          #89
    cover = Column(Unicode(128))        #57
    rating = Column(Integer)            #0-100

