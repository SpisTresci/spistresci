import nose
from nose.tools import *
from utils import NoseUtils

from xml.etree import ElementTree as et
from connectors.specific import Nexto
import os

class TestSpecificConnectors():

    def setUp(self):
        Nexto.config_file = 'unittests/data/specific_connectors/conf/test.ini'

    def tearDown(self):
        pass

    def test_nexto_make_dict(self):
        nexto = Nexto()

        filename = os.path.join(nexto.backup_dir, nexto.filename)
        print nexto.backup_dir, nexto.filename
        root = et.parse(filename).getroot()
        offers = list(root)
        dic = nexto.makeDict(offers[0])

        dic2 = {
                'default_price': u'1.62',
                'publisher': u'NetPress Digital Sp. z o.o.',
                'product_code': u'netpress_pbi_08429',
                'isbn': u'netpress_pbi_08429',
                'description': u'description',
                'title': u'Skarb wata\u017cki : powie\u015b\u0107 z ko\u0144ca XVIII wieku',
                'format':   {
                            'protection': u'NO_DRM',
                            'properties': u'None',
                            'format': u'epub'
                            },
                'cover': u'http://www.nexto.pl/upload/sklep/netpress/pbi/ebook/skarb_watazki__powiesc_z_konca_xviii_wie-wladyslaw_lozinski-netpress_digital/public/cover-6833.jpg',
                'default_spread': u'59.88',
                'gross_price': u'1.99',
                'issue_id': u'56368',
                'lang_short': u'pl',
                'authors': u'W\u0142adys\u0142aw \u0141ozi\u0144ski',
                'manufacturer_id': u'9',
                'category_id':  [
                                    u'1212',
                                    u'1015'
                                ],
                'external_id': u'27138',
                'vat': u'23',
                'api_price': u'0.65'
                }

        eq_(dic, dic2)
