import nose
from nose.tools import *

from connectors.Tools import *
from connectors import GenericConnector

        

class FilterableConnector(GenericConnector):
    def applySingleFilter(self, filter_name, f_params):
        self.filters_applied.append(filter_name)


@notFilterableConnector
class NotFilterableConnector(FilterableConnector):
    pass

class TestNotFilterableConnector():

    def setUp(self):
        FilterableConnector.config_file = 'unittests/data/connectors_tools/conf/test.ini'
        self.filters = 'a,b,c,d'

    def tearDown(self):
        pass

    @raises(NotImplementedError)
    def test_not_filterable_connector(self):
        self.connector = NotFilterableConnector()
        self.connector.filters = self.filters
        self.connector.applyFilters()

    def test_filterable_connector(self):
        self.connector = FilterableConnector()
        self.connector.filters_applied = []
        self.connector.filters = self.filters
        self.connector.applyFilters()
        eq_(self.filters, ','.join(self.connector.filters_applied))
