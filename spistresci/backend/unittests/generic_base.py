from connectors.generic import GenericBase
from nose.tools import *

class MockContext(GenericBase):
    @classmethod
    def _name(cls):
        return cls.__name__
    @property
    def name(self):
        return self._name()

    def __init__(self):
        self.register()

class MockAuthor(MockContext):
    pass

class MockBook(MockContext):
    pass

class MockBooksAuthors(MockContext):
    pass

class MockBookDescription(MockContext):
    pass


class TestGenericBase(object):
    @classmethod
    def setUpClass(cls):
        cls.ma = MockAuthor()
        cls.mb = MockBook()
        cls.mba = MockBooksAuthors()

    def assertGetConcretizedClass(self, mock):
        eq_(mock.getConcretizedClass(mock, 'Book'), MockBook)
        eq_(mock.getConcretizedClass(mock, 'Author'), MockAuthor)
        eq_(mock.getConcretizedClass(mock, 'BooksAuthors'), MockBooksAuthors)

    def testGetConcretizedClass(self):
        self.assertGetConcretizedClass(self.ma)
        self.assertGetConcretizedClass(self.mb)
        self.assertGetConcretizedClass(self.mba)
