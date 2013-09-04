from utils import filter_varargs
from utils import Str
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



class TestStr(object):
    def setUp(self):
        pass
    def test_list_to_unicode(self):
        eq_(Str.listToUnicode(None), None)
        eq_(Str.listToUnicode('dummy'), u'dummy')
        eq_(Str.listToUnicode(1), u'1')
        eq_(Str.listToUnicode(['one', 'two', 'three']), u'one, two, three')
        eq_(Str.listToUnicode([1,2,3]), u'1, 2, 3')
        eq_(Str.listToUnicode([1,2,3],'_separator_'), u'1_separator_2_separator_3')

