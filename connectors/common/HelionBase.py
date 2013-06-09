from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *


class HelionBase(XMLConnector):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        "./isbn":('isbns', ''),
        "./ean":('ean', ''),
        "./ident":('external_id', ''),
        "./tytul[@language='polski']":('title', ''),
        "./tytul[@language='oryginal']":('title_oryginal', ''),
        "./link":('url', ''),
        "./autor":('authors', ''),
        "./tlumacz":('translators', ''),
        "./status":('is_available', 0),
        "./cena":('price', 0),
        "./cenadetaliczna":('price_normal', ''),
        "./znizka":('discount', ''),
        "./marka":('bookshop', ''),
        "./nazadanie":('on_demand', ''),
        "./format":('book_size', ''),
        "./ebook_formaty/ebook_format":('formats', ''),
        "./typ":('type', ''),
        "./oprawa":('binding', ''),
        "./liczbastron":('page_count', ''),
        "./datawydania":('date', ''),
        "./online":('free_sample_url', ''),
        "./okladka":('cover', ''),
        "./okladkatyl":('cover_back', ''),
        "./issueurl":('free_fragment_online_tool', ''),
        "./bestseller":('is_bestseller', ''),
        "./nowosc":('is_new', ''),
        "./promocja":('name_of_promotion', ''),
        "./powiazane/ident_powiazany":('linked', ''), #        "./powiazane":('related', ''),
        "./serietematyczne/serietematyczna":('thematic_series', ''),
        "./seriewydawnicze/seriawydawnicza":('series', ''),
        "./ksiegarnie_nieinter/waga":('mass', ''),
        "./ksiegarnie_nieinter/status2":('status2', ''),
        "./ksiegarnie_nieinter/cena_netto":('net_price', ''),
        "./ksiegarnie_nieinter/cena_brutto":('gross_price', ''),
        "./ksiegarnie_nieinter/vat":('vat', ''),
        "./ksiegarnie_nieinter/vat_procent":('vat_percent', ''),
        "./opis":('description', ''),
        "./top":('place_in_top', ''),
        "./przedsprzedazDO":('advanced_booking',''),
        "./nosnik":('storage_type',''),
        "./md5":('md5', ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("./lista[@baza='" + self.name.lower() + "']")[0]

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, 'discount')
        super(HelionBase, self).validate(dic)


class HelionBaseBook(GenericBook):
    external_id = Column(Unicode(16), unique=True)
    #isbn
    ean = Column(Unicode(16))                          #14
    title = Column(Unicode(256))                       #186
    title_oryginal = Column(Unicode(256))              #177
    url = Column(Unicode(512))                         #278
    #authors
    #translators
    #status
    #price
    #price_normal
    discount = Column(Integer)                         #GROSZE!!!
    bookshop = Column(Integer)
    on_demand = Column(Integer) #TODO: T284
    book_size = Column(Unicode(128))                   #79!
    #formats
    type = Column(Integer)
    binding = Column(Unicode(8))                       #6
    page_count = Column(Integer)
    date = Column(Date)
    free_sample_url = Column(Unicode(64))              #44
    cover = Column(Unicode(64))                        #49
    cover_back = Column(Unicode(64))                   #51
    free_sample_online_tool_url = Column(Unicode(64))  #46
    is_bestseller = Column(Boolean)
    is_new = Column(Boolean)
    name_of_promotion = Column(Unicode(128))           #29
    #linked    #TODO: T285
    #thematic_series
    #series

    #add support for paper books
    #
    #    "./ksiegarnie_nieinter/waga":('mass', ''),
    #    "./ksiegarnie_nieinter/status2":('status2', ''),
    #    "./ksiegarnie_nieinter/cena_netto":('net_price', ''),
    #    "./ksiegarnie_nieinter/cena_brutto":('gross_price', ''),
    #    "./ksiegarnie_nieinter/vat":('vat', ''),
    #    "./ksiegarnie_nieinter/vat_procent":('vat_percent', ''),

    advanced_booking = Column(Date)
    #description
    place_in_top = Column(Integer)
    storage_type = Column(Unicode(16))                  #9
    md5 = Column(Unicode(32))                           #32

