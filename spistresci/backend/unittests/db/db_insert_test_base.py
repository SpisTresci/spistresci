from nose.tools import *
from connectors.generic import GenericBook
from models import UpdateStatus, UpdateStatusService
from . import LocalSqlWrapper
from utils.NoseUtils import neq_

class DBInsertTestBase(object):
    def setUp(self):
        self.connector = self.connector_class()
        self.connector.session = LocalSqlWrapper.getSession()
        self.us = UpdateStatus(session=self.connector.session)

    def __init__(self):
        self.check_counter = 0

    def _check_if_eq(self, list_of_dicts, insert_file=None):
        uss = UpdateStatusService(self.us, self.connector)

        if insert_file == None:
            insert_file = 'unittests/data/db/update/xml/' + self.connector.name.lower() + str(self.check_counter) + '.xml'

        self.check_counter += 1
        self.connector.fetched_files = [insert_file]
        self.connector.parse()
        self.connector.session.commit()
        self._check(list_of_dicts, eq_)

        uss.success = True

    def _check_if_not_eq(self, list_of_dicts):
        self._check(list_of_dicts, neq_)

    def _check(self, list_of_dicts, op_):
        Book = GenericBook.getConcretizedClass(context=self.connector)

        for dic in list_of_dicts:
            book = self.connector.session.query(Book).filter_by(**{"external_id":dic['external_id']}).first()
            assert book != None

            for key in dic.keys():
                if key == "authors":
                    eq_(len(dic["authors"]), len((book.authors)))
                    for a1, a2 in zip(dic["authors"], book.authors):
                        op_(a1, a2.name)

                elif key != "external_id":
                    op_(dic[key], getattr(book, key))


    def test_tables_created(self):
        eq_(LocalSqlWrapper.getEngine().name, 'mysql')
        defined_tables = LocalSqlWrapper.getEngine().table_names()
        generic_tables = ['%s%s' % (self.connector.name, table) for table in 'Author', 'Book', 'BookPrice', 'BooksAuthors', 'ISBN', 'BooksFormats', 'Format']
        ok_(all(generic in defined_tables for generic in generic_tables))
