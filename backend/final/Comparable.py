from sqlwrapper import *
from final.BaseCompare import BaseCompare
Base = SqlWrapper.getBaseClass()

def cmp(obj1, obj2):
    if not obj1 or not obj2:
        return (0.8, False)

    return obj1.cmp(obj2)

def cmp_lists(list1, list2):
    r = Comparable.Result()
    max_len = 0 if not list1 or not list2 else max(len(list1), len(list2))

    if max_len == 0:    #TODO: musza byc tutaj wprowadzone wagi, by brak wszystkich atrybutow do porownania nie powodowal mergowania
        return 0.8

    for obj1 in list1:
        for obj2 in list2:
            r.add(obj1.cmp(obj2))

    return r.matches()/float(max_len)


class Comparable(object):
    accept_threshold = 1.0

    def __init__(self, *args, **kwargs):
        super(Comparable, self).__init__(*args, **kwargs)

    def cmp(self, other):
        raise NotImplementedError

    def cmp_with_list(self, l_others):
        for other in l_others:
            self.cmp(other)

    class Result():
        def __init__(self):
            self.tests = []

        def add(self, (ratio, merged)):
            self.tests.append((ratio, merged))

        def addRatio(self, ratio):
            self.tests.append((ratio, False))

        def result(self):
            return self.geo_avg([r for r, m in self.tests])

        def __repr__(self):
            return str(self.result())

        def matches(self):
            return len([m for r, m in self.tests if m])

        @staticmethod
        def geo_avg(tests):
            if len(tests) == 0:
                return 0.0

            r = 1.0
            for t in tests:
                r *= t

            return r ** (1.0 / len(tests))

        @staticmethod
        def avg(tests):
            if len(tests) == 0:
                return 0.0

            return sum(tests) / float(len(tests))

    @declared_attr
    def declareCache(cls):
        cache_name = "%sCompare" % cls.__name__
        exec('class %s(BaseCompare, Base): pass' % cache_name)
        exec('cls.cache = %s' % cache_name)
        SqlWrapper.table_list += [cache_name]
