# -*- coding: utf-8 -*-
import nose
from nose.tools import *
from utils import NoseUtils
from utils import SimilarityCalculator as SC


class DummyData():
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

class TestSimilarityCalculator():

    def test_name(self):
        ok_(True)

    def test_isInitial(self):
        yield eq_, SC.isInitial("H."), True
        yield eq_, SC.isInitial("A."), True
        yield eq_, SC.isInitial("A."), True

        yield eq_, SC.isInitial(u"\u0104."), True
        yield eq_, SC.isInitial(u"\u0105."), False
        yield eq_, SC.isInitial(u"Ą."), True
        yield eq_, SC.isInitial(u"ą."), False

        yield eq_, SC.isInitial("Ą."), False
        yield eq_, SC.isInitial("ą."), False

        yield eq_, SC.isInitial("a."), False
        yield eq_, SC.isInitial("A"), False
        yield eq_, SC.isInitial("Z"), False
        yield eq_, SC.isInitial("g"), False
        yield eq_, SC.isInitial("s"), False

        yield eq_, SC.isInitial(".."), False
        yield eq_, SC.isInitial("RG"), False
        yield eq_, SC.isInitial("KE."), False
        yield eq_, SC.isInitial(".E."), False
        yield eq_, SC.isInitial("G "), False
        yield eq_, SC.isInitial("G W"), False
        yield eq_, SC.isInitial("G. W."), False
        yield eq_, SC.isInitial("G.E."), False

    def test_isInitialAndName(self):
        yield eq_, SC.isInitialAndName("A.", "Artur"), True
        yield eq_, SC.isInitialAndName("Artur", "A."), True

        yield eq_, SC.isInitialAndName("A.", "Bartek"), True
        yield eq_, SC.isInitialAndName("Bartek", "A."), True

        yield eq_, SC.isInitialAndName("A.", "A."), False
        yield eq_, SC.isInitialAndName("A.", "B."), False

        yield eq_, SC.isInitialAndName("A", "Adam"), False
        yield eq_, SC.isInitialAndName("Adam", "A"), False

        yield eq_, SC.isInitialAndName(u"Ć.", u"Ćma"), True
        yield eq_, SC.isInitialAndName(u"Ćma", u"Ć."), True

        yield eq_, SC.isInitialAndName("Ć.", "Ćma"), False
        yield eq_, SC.isInitialAndName("Ćma", "Ć."), False

        yield eq_, SC.isInitialAndName("Ć.", u"Ćma"), False
        yield eq_, SC.isInitialAndName(u"Ćma", "Ć."), False

        yield eq_, SC.isInitialAndName(u"Ć.", "Ćma"), True
        yield eq_, SC.isInitialAndName("Ćma", u"Ć."), True

        yield eq_, SC.isInitialAndName(u"Ą.", u"Ąż"), True
        yield eq_, SC.isInitialAndName(u"Ą", u"Ąż"), False

        yield eq_, SC.isInitialAndName(u"Ą.", u"Aż"), True
        yield eq_, SC.isInitialAndName("A", u"Ąż"), False

    def test_equal_authors(self):
        """yield ok_, SC.eq_authors(DummyData({"name":"Adrian K. Antosik", "firstName":"Adrian", "middleName":"K.", "lastName":"Antosik"}),
                                      DummyData({"name":"Adrian Antosik", "firstName":"Adrian", "middleName": "", "lastName":"Antosik"}))

        yield ok_, SC.eq_authors(DummyData({"name":"P. C Cast", "firstName":"P.", "middleName":"C", "lastName":"Cast"}),
                                      DummyData({"name":"P. C. Cast", "firstName":"P.", "middleName": "C.", "lastName":"Cast"}))"""
        pass

    def test_equal_isbns(self):
        """
        yield ok_, SC.eq_isbns(DummyData({"raw":"978-83-7902-024-9", "core":"837902024", "isbn10":"8379020243", "isbn13":"9788379020249", "valid":"1"}),
                                    DummyData({"raw":"83-7902-024-3", "core":"837902024", "isbn10":"8379020243", "isbn13":"9788379020249", "valid":"1"}))

        yield ok_, SC.eq_isbns(DummyData({"raw":"978-83-7902-024-9", "core":"837902024", "isbn10":"8379020243", "isbn13":"9788379020249", "valid":"1"}),
                                    DummyData({"raw":"83-7902-024-9", "core":u"", "isbn10":u"", "isbn13":u"", "valid":"0"}))
        """
        pass
