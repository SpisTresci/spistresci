from spistresci.connectors.common import Ceneo
import re


class Gandalf(Ceneo):
    #dict of xml_tag -> db_column_name translations
    xml_tag_dict = {
        'external_id':('@id', ''),
        'url':('@url', ''),
        'price':('@price', 0),
        'availability': ('@avail', ''),
        'category':('./cat', ''),
        'title':('./name', ''),
        'cover':("./imgs/main/@url", ''),
        'description':('./desc', ''),

        'authors':("./attrs/a[@name='Autor']", ''),
        'isbns':("./attrs/a[@name='ISBN']", ''),
        #'eans':("./attrs/a[@name='EAN']", ''), this information like ISBN, but in different format
        'formats':("./attrs/a[@name='Format']", ''),
        'page_count':("./attrs/a[@name='Ilosc_stron']", ''),
        'cover_type':("./attrs/a[@name='Oprawa']", ''),
        'publisher':("./attrs/a[@name='Wydawnictwo']", ''),
    }

    def weHaveToGoDeeper(self, root, depth):
        return root.xpath("./group[@name='books']")[0]

    def validateTitle(self, dic, id, title):
        for format in dic['formats']:
            dic['title'] = re.sub('\W'+format['name'].lower()+'$', '', dic['title'])
