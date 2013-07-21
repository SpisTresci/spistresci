from connectors.generic import *
import lxml.etree as et
from sqlwrapper import *


class HelionBase(XMLConnector):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'isbns': ('./isbn', ''),
        'ean': ('./ean', ''),
        'external_id': ('./ident', ''),
        'title': ("./tytul[@language='polski']", ''),
        'title_oryginal': ("./tytul[@language='oryginal']", ''),
        'url': ('./link', ''),
        'authors': ('./autor', ''),
        'translators': ('./tlumacz', ''),
        'is_available': ('./status', 0),
        'price': ('./cena', 0),
        'price_normal': ('./cenadetaliczna', ''),
        'discount': ('./znizka', ''),
        'bookshop': ('./marka', ''),
        'on_demand': ('./nazadanie', ''),
        'book_size': ('./format', ''),
        'formats': ('./ebook_formaty/ebook_format', ''),
        'type': ('./typ', ''),
        'binding': ('./oprawa', ''),
        'page_count': ('./liczbastron', ''),
        'date': ('./datawydania', ''),
        'free_sample_url': ('./online', ''),
        'cover': ('./okladka', ''),
        'cover_back': ('./okladkatyl', ''),
        'free_fragment_online_tool': ('./issueurl', ''),
        'is_bestseller': ('./bestseller', ''),
        'is_new': ('./nowosc', ''),
        'name_of_promotion': ('./promocja', ''),
        'linked': ('./powiazane/ident_powiazany', ''), 
        'thematic_series': ('./serietematyczne/serietematyczna', ''),
        'series': ('./seriewydawnicze/seriawydawnicza', ''),
        'mass': ('./ksiegarnie_nieinter/waga', ''),
        'status2': ('./ksiegarnie_nieinter/status2', ''),
        'net_price': ('./ksiegarnie_nieinter/cena_netto', ''),
        'gross_price': ('./ksiegarnie_nieinter/cena_brutto', ''),
        'vat': ('./ksiegarnie_nieinter/vat', ''),
        'vat_percent': ('./ksiegarnie_nieinter/vat_procent', ''),
        'description': ('./opis', ''),
        'place_in_top': ('./top', -1),
        'advanced_booking': ('./przedsprzedazDO', None),
        'storage_type': ('./nosnik', ''),
        'md5': ('./md5', ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("./lista[@baza='" + self.name.lower() + "']")[0]

    def validate(self, dic):
        id = dic.get('external_id')
        title = dic.get('title')
        self.validatePrice(dic, id, title, 'discount')
        super(HelionBase, self).validate(dic)

    
    #statuses = {
    #            0:('unavailable', 'niedostepna'),
    #            1:('available', 'dostepna'),
    #            2:('in preparation', 'w przygotowaniu'),
    #            3:('presale', 'przedsprzedaz'),
    #            4:('print on demand', 'druk na zadanie'),
    #            5:('few pieces left in stock', 'dostepna w malej ilosci'),
    #            }

class HelionBaseBook(GenericBook):

    external_id = Column(Unicode(16), unique=True)
    #isbn
    ean = Column(Unicode(16))                          #14
    title = Column(Unicode(256))                       #186
    title_oryginal = Column(Unicode(256))              #177
    url = Column(Unicode(512))                         #278
    #authors
    #translators
    status = Column(Integer)
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

