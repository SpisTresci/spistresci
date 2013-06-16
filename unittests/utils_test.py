from utils import filter_varargs
from nose.tools import *

class TestFilterVarargs(object):
    def setUp(self):
        self.true = lambda x,y,z:True
        self.false = lambda x,y,z:False
        self.same = lambda x,y,z:x
    def test_filter_varargs(self):
        eq_(filter_varargs(self.true, [1,2,3,4], True, 'dummy','dummy'),[1,2,3,4])
        eq_(filter_varargs(self.true, [1,2,3,4], False, 'dummy','dummy'),[])
        eq_(filter_varargs(self.false, [1,2,3,4], False, 'dummy','dummy'),[1,2,3,4])
        eq_(filter_varargs(self.false, [1,2,3,4], True, 'dummy','dummy'),[])
        eq_(filter_varargs(self.same, [0,False,1,True], False, 'dummy','dummy'),[0 , False])
        eq_(filter_varargs(self.same, [0,False,1,True], True, 'dummy','dummy'),[1, True])


