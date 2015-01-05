from connectors.generic import *
from spistresci.connectors.utils.Str import listToUnicode


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
        'size': ('./format', ''),
        'formats': ('./ebook_formaty/ebook_format', ''),
        'type': ('./typ', ''),
        'binding': ('./oprawa', ''),
        'page_count': ('./liczbastron', ''),
        'date': ('./datawydania', ''),
        'sample': ('./online', ''),
        'cover': ('./okladka', ''),
        'cover_back': ('./okladkatyl', ''),
        'online_sample': ('./issueurl', ''),
        'is_bestseller': ('./bestseller', ''),
        'is_new': ('./nowosc', ''),
        'promotion_name': ('./promocja', ''),
        'linked': ('./powiazane/ident_powiazany', ''), 
        'thematic_series': ('./serietematyczne/seriatematyczna', ''),
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

    def adjust_parse(self, dic):
        for key in ['promotion_name', 'thematic_series', 'series', 'linked']:
            dic[key] = listToUnicode(dic.get(key))

    
    #statuses = {
    #            0:('unavailable', 'niedostepna'),
    #            1:('available', 'dostepna'),
    #            2:('in preparation', 'w przygotowaniu'),
    #            3:('presale', 'przedsprzedaz'),
    #            4:('print on demand', 'druk na zadanie'),
    #            5:('few pieces left in stock', 'dostepna w malej ilosci'),
    #            }

# class HelionBaseBook(GenericBook):
#     external_id = Column(Unicode(16), unique=True)
#     #isbn
#     ean = Column(Unicode(16))                          #14
# #    title = Column(Unicode(256))                       #120
#     title_oryginal = Column(Unicode(256))              #177
#     #url
#     #cover
#     cover_back = Column(STUrl)                   #51
#     #authors
#     #translators
#     #formats
#     #description
#     status = Column(Integer)
#     #price
#     #price_normal
#     discount = Column(Integer)                         #GROSZE!!!
#     bookshop = Column(Integer)
#     on_demand = Column(Integer) #TODO: T284
#     size = Column(Unicode(64))                   #33
#     type = Column(Integer)
#     binding = Column(Unicode(16))                       #6
#     page_count = Column(Unicode(8))
#     date = Column(Date)
#     sample = Column(STUrl)              #44
#     online_sample = Column(STUrl)  #44
#     is_bestseller = Column(Boolean)
#     is_new = Column(Boolean)
#     name_of_promotion = Column(Unicode(128))           #29
#     linked = Column(Unicode(128))                                            #12 X 5 #TODO: T285
#     #thematic_series
#     #series
#
#     #add support for paper books
#     #
#     #    "./ksiegarnie_nieinter/waga":('mass', ''),
#     #    "./ksiegarnie_nieinter/status2":('status2', ''),
#     #    "./ksiegarnie_nieinter/cena_netto":('net_price', ''),
#     #    "./ksiegarnie_nieinter/cena_brutto":('gross_price', ''),
#     #    "./ksiegarnie_nieinter/vat":('vat', ''),
#     #    "./ksiegarnie_nieinter/vat_procent":('vat_percent', ''),
#
#     advanced_booking = Column(Date)
#     place_in_top = Column(Integer)
#     storage_type = Column(Unicode(16))                  #4
#     md5 = Column(Unicode(32))                           #32

