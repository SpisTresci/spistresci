from connectors.generic import *
from sqlwrapper import *
import os


class Virtualo(XMLConnector):

    depth=0
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        './coverId' : ('external_id', ''),
        './title' : ('title', ''),
        './format' : ('format', ''),
        './security' : ('protection', ''),
        './price' : ('price', 0),
        './isbn' : ('isbn', ''),
        './authors' : ('authors', ''),
        './url' : ('url', ''),
        './description' : ('description', ''),
        #not added to database
        './descriptionShort' : ('descriptionShort', ''),
        './rating' : ('rating', ''),
     }

    def validate(self, dic):
        super(Virtualo, self).validate(dic)
        self.validateRating(dic)

    def validateRating(self, dic, rating_tag='rating'):
        rating = dic.get(rating_tag, '0')
        rating_normalized = 0
        try:
            #normalize ratings 1-5 -> %
            rating_normalized = str(int(20 * float(rating.replace(',', '.'))))
        except ValueError:
            self.erratum_logger.warning('Entry has invalid rating. Connector: %s, id: %s, title: %s' % (self.name, dic.get('external_id'), dic.get('title')))
        finally:
            dic[rating_tag] = rating_normalized


Base = SqlWrapper.getBaseClass()

class VirtualoBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(256))        #174
    format = Column(Unicode(8))         #6
    protection = Column(Unicode(8))       #3
    price = Column(Integer)             #*0,01PLN
    isbn = Column(Unicode(13))          #0
    url = Column(Unicode(128))          #89
    rating = Column(Integer)            #0-100


class VirtualoBookDescription(GenericBookDescription, Base):
    pass

class VirtualoAuthor(GenericAuthor, Base):
    pass

class VirtualoBookPrice(GenericBookPrice, Base):
    pass

class VirtualoBooksAuthors(GenericBooksAuthors, Base):
    pass

