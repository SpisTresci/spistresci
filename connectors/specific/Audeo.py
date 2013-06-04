from connectors.generic import *
from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Audeo(Ceneo):
    
#    xmls_namespace = {"n" : "http://www.w3.org/2001/XMLSchema-instance"} 
    
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict= {
        "@id":('external_id',''),
        "@price":('price', 0),
        "@url":('url',''),
        "@avail":('availability',''),
        "./cat":('category',''),
        "./name":('title',''),
        "./imgs/main[@url]":('cover',''),
        "./desc":('description',''),
        "./attrs/a[@name='Producent']":('producent',''),
        "./attrs/a[@name='Autor']":('authors',''),
        "./attrs/a[@name='Lektor']":('lectors',''),
        "./attrs/a[@name='Czas (min)']":('time',''),
    }

    #Try getting authors from description
    def getAuthorsFromDescription(self, dic, name):
        #TODO: Not implemented yet        
        pass

    def adjust_parse(self, dic):
        if dic['authors'] == ['Praca Zbiorowa'] or dic['authors'] == ['Zbiorowy']:
            self.getAuthorsFromDescription(dic, u"Autor", "authors")


class AudeoBook(GenericBook, Base):
    id = Column(Integer, primary_key=True)
    price = Column(Integer)             #GROSZE!!!
    url = Column(Unicode(256))           #152
    availability = Column(Integer)
    category = Column(Unicode(64))      #33
    title = Column(Unicode(256))        #136
    cover = Column(Unicode(128))        #118
    time = Column(Integer)
    producent = Column(Unicode(64))     #35

