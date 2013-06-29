from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

Base = SqlWrapper.getBaseClass()

class Pokatne(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./id":('external_id', ''),
        "./title":('title', ''),
        "./authors":('authors', ''),
        "./url":('url', ''),
        "./cover":('cover', ''),
        "./formats":('formats', ''),
        "./date":('date', ''),
        "./comments":('comments', ''),
        "./views":('views', ''),
        "./rating":('rating', ''),
        "./votes":('votes', ''),
        "./alert":('alert', ''),
        "./tags":('tags', ''),
        "./new":('new', ''),
    }

    def validate(self, dic):
        self.validateRating(dic)
        super(Pokatne, self).validate(dic)

    def validateRating(self, dic):
        rating = dic.get('rating')
        if rating:
            dic['rating'] = int(round(float(dic['rating']), 1) * 10)

class PokatneBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    #external_id
    title = Column(Unicode(128))        #63
    #authors
    url = Column(Unicode(64))           #49
    cover = Column(Unicode(64))         #48
    #formats
    date = Column(Unicode(10))          #10
    comments = Column(Integer)
    views = Column(Integer)
    rating = Column(Integer)
    votes = Column(Integer)
    alert = Column(Boolean)
    tags = Column(Unicode(64))          #59
    new = Column(Boolean)

