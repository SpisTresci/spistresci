from spistresci.connectors.common import Ceneo

class Woblink(Ceneo):

    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id': ('@id', ''),
        'price': ('@price', 0),
        'url': ('@url', ''),
        'availability': ('@avail', ''),
        'category': ('./cat', ''),
        'title': ('./name', ''),
        'cover': ('./imgs/main/@url', ''),
        'description': ('./desc', ''),
        'isbns': ("./attrs/a[@name='ISBN']", ''),
        'publisher': ("./attrs/a[@name='Wydawnictwo']", ''),
        'formats': ("./attrs/a[@name='Format']", ''),
    }
