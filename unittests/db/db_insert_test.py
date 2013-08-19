# -*- coding: utf-8 -*-
from unittests.db.db_insert_test_base import DBInsertTestBase
from connectors.specific.Audiobook import Audiobook

class TestAudiobookUpdate(DBInsertTestBase):
    config_file = 'unittests/data/db/update/conf/audiobook.ini'
    connector_class = Audiobook

    def test_Audiobook(self):

        self._check_if_eq( [{
            "external_id":256,
            "title": u"MAŁY KSIĄŻĘ",
            "category": u"LITERATURA ŚWIATOWA/Klasyka światowa",
            "price": 3591,
            "url": "https://www.a4b-tracking.com/pl/stat-click-feed/20602637/33",
            "authors":[u"Antoine de Saint-Exupery"],
            "length": 108,
            "publisher": "AudioLiber",
        }])

        self._check_if_eq([{
                "external_id":256,
                "title": u"MAŁY KSIĄŻĘ",
                "category": u"LITERATURA ŚWIATOWA/Klasyka światowa",
            "price": 1000,
                "url": "https://www.a4b-tracking.com/pl/stat-click-feed/20602637/33",
                "authors":[u"Antoine de Saint-Exupery"],
            "length": 128,
                "publisher": "AudioLiber",
        }])

        self._check_if_eq([{
                "external_id":256,
            "title": u"Mały Książe",
                "category": u"LITERATURA ŚWIATOWA/Klasyka światowa",
            "price": 4000,
                "url": "https://www.a4b-tracking.com/pl/stat-click-feed/20602637/33",
                "authors":[u"Antoine de Saint-Exupery"],
                "length": 128,
                "publisher": "AudioLiber",
        }])

        self._check_if_not_eq([{
                "external_id":256,
                "price": 1000,
        }])