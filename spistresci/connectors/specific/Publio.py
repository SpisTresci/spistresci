from spistresci.connectors.generic import XMLConnector
from spistresci.connectors.utils.Str import listToUnicode


class Publio(XMLConnector):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('./id', ''),
        'title': ('./title', ''),
        'authors': ('./authors', ''),
        'formats': ('./formats', ''),
        'protection': ('./protectionType', ''),  #???
        'price': ('./price', ''),
        'url': ('./productUrl', ''),
        'cover': ('./imageUrl', ''),
        'isbns': ('./isbns', ''),
        'publisher': ('./company', ''),
        'category': ('./categories/category', ''),
    }

    def adjust_parse(self, dic):
        #convert category to list
        dic['category'] = listToUnicode(dic.get('category'))

    def validateISBNs(self, dic, id, title):
        if 'isbns' in dic:
            dic['isbns'] = [isbn.strip() for isbn in dic['isbns'].split(',')]

        super(Publio, self).validateISBNs(dic, id, title)
