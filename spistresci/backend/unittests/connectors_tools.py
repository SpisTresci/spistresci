import nose
from nose.tools import *

from connectors.Tools import *
from connectors import GenericConnector
from utils import filter_varargs
from utils import ConfigReader


class FilterableConnector(GenericConnector):
    def applySingleFilter(self, filter_name, f_params):
        self.filters_applied.append(filter_name)


@notFilterableConnector
class NotFilterableConnector(FilterableConnector):
    pass

class TestNotFilterableConnector(object):

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


class TestFilterFunctions(object):

    def setUp(self):
        self.config = ConfigReader.read_config('unittests/data/connectors_tools/conf/test.ini')

    def test_filter_in_list(self):
        eq_(filter_in_list((1,'x'), [2,3]), False)
        ok_(filter_in_list((1,'x'), [1,2,3,5,1]))
        ok_(filter_in_list((1,'x'), None))

    def test_filter_disabled(self):
        eq_(filter_disabled(('MockEnabledConnector','x'), self.config), False)
        eq_(filter_disabled(('MockEnabledConnector1','x'), self.config), False)
        ok_(filter_disabled(('MockDisabledConnector','x'), self.config))
        ok_(filter_disabled(('MockDisabledConnector1','x'), self.config))
        ok_(filter_disabled(('MockDisabledConnector2','x'), self.config))

    def test_filter_in_list_varargs(self):
        eq_(filter_varargs(filter_in_list, [(1, 'x'), (2, 'x'), (3, 'x')], True, [1,2,4]), [(1, 'x'), (2, 'x')])
        eq_(filter_varargs(filter_in_list, [(1, 'x'), (2, 'x'), (3, 'x')], True, None), [(1, 'x'), (2, 'x'), (3,'x')])
        eq_(filter_varargs(filter_in_list, [(1, 'x'), (2, 'x'), (3, 'x')], False, None), [])
        eq_(filter_varargs(filter_in_list, [(1, 'x'), (2, 'x'), (3, 'x')], False, [1,2,4]), [(3, 'x')])

    def test_filter_disabled_varargs(self):
        self.e = 'MockEnabledConnector'
        self.e1 = 'MockEnabledConnector1'
        self.d = 'MockDisabledConnector'
        self.d1 = 'MockDisabledConnector1'
        self.d2 = 'MockDisabledConnector2'
        self.con_list = [(x,'x') for x in [self.e, self.e1, self.d, self.d1, self.d2]]
        eq_(filter_varargs(filter_disabled, self.con_list, True, self.config),[(self.d,'x'), (self.d1,'x'), (self.d2,'x')])
        eq_(filter_varargs(filter_disabled, self.con_list, False, self.config),[(self.e,'x'), (self.e1,'x')])
