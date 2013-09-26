from connectors.generic import XMLConnector
from sqlwrapper import *
from connectors.generic import GenericBook

class TaniaKsiazka(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'awId': ("@awId", ''),
        'programName': ('@programName', ''),
        'external_id': ('./pId', None),
        'title': ('./name', ''),
        'description': ('./desc', ''),
        'category_id': ('./cat/awCatId', ''),
        'category': ('./cat/awCat', ''),
        'type': ('./cat/mCat', ''),
        'brand': ('./brand', ''),
        'url': ('./awLink', ''),
        'thumbnail': ('./awThumb', ''),
        'cover': ('./awImage', ''),
        'price': ('./price/display',  0),
        'isbns': ("./atribute[@Name='ISBN']", ''),
       }

    #TODO: we don't know how to get formats (YET)
    def adjust_parse(self, dic):
        dic['formats'] = ['unknown']

Base = SqlWrapper.getBaseClass()

class TaniaKsiazkaBook(GenericBook, Base):
    id = Column(Integer, primary_key = True)
    category = Column(Unicode(32))          #22
    title = Column(Unicode(256))            #200
    url = Column(Unicode(512))              #284
    type = Column(Unicode(64))              #51
    price = Column(Integer)                 #grosze
    cover = Column(Unicode(64))             #46
    thumbnail = Column(Unicode(64))         #47
    programName = Column(Unicode(32))       #16
    category_id = Column(Integer)           #
    brand = Column(Unicode(32))             #?
    awId = Column(Integer)                  #

