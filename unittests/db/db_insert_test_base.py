from nose.tools import *
from connectors.generic import GenericConnector, GenericBook
from sqlwrapper import SqlWrapper
from sqlalchemy.orm import sessionmaker
import utils
from utils.NoseUtils import neq_

class DBInsertTestBase(object):

    @classmethod
    def setUpClass(cls):
        cls.connectors = [cls.connector_class.class_name()]
        cls.connector = cls.connector_class()

        SqlWrapper.init(config_file=cls.config_db_file, connectors=cls.connectors)
        cls.engine = SqlWrapper.getEngine()
        cls.Session = sessionmaker(bind=cls.engine, autoflush=False)
        cls.connector.createSession()

    @classmethod
    def tearDownClass(cls):
        cls.connector.closeSession()

    def __init__(self):
        self.check_counter = 0

    def _check_if_eq(self, list_of_dicts, insert_file=None):
        if insert_file == None:
            insert_file = 'unittests/data/db/update/xml/' + self.connector.name.lower() + str(self.check_counter) + '.xml'

        self.check_counter += 1
        self.connector.fetched_files = [insert_file]
        self.connector.parse()
        self.connector.session.commit()

        self._check(list_of_dicts, eq_)

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
        eq_(self.engine.name, 'mysql')
        t1 = self.engine.table_names()
        t2 = ['%s%s' % (self.connector_class.class_name(), table) for table in 'Author', 'Book', 'BookDescription', 'BookPrice', 'BooksAuthors', 'ISBN', 'BooksFormats', 'Format']

        t2 += [
                    'MasterAuthor',
                    'MasterBook',
                    'MasterISBN',
                    'MiniAuthor',
                    'MiniBook',
                    'MiniISBN',
                    'PersonRole',
                    'SoundexTitleWord',
                    'TitleWord',
                    'master_books_master_authors',
                    'master_books_master_isbns',
                    'master_books_title_words',
                    'mini_books_mini_authors',
                    'mini_books_mini_isbns',
                    'mini_books_title_words'
                ]

        t1.sort()
        t2.sort()
        for tb1, tb2 in zip(t1, t2):
            eq_(tb1, tb2)
