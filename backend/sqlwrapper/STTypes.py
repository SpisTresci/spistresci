import sqlalchemy


class STUnicode(sqlalchemy.Unicode):
    class comparator_factory(sqlalchemy.Unicode.Comparator):
        def isSimilar(self, other):
            return sqlalchemy.sql.func.levenshtein(self.expr, other) < 4

class STUnicode10(sqlalchemy.Unicode):
    class comparator_factory(sqlalchemy.Unicode.Comparator):
        def isSimilar(self, other):
            return sqlalchemy.sql.func.levenshtein(self.expr, other) < 10

class STUrl(sqlalchemy.Unicode):
    def __init__(self, length=2048, **kwargs):
        super(sqlalchemy.Unicode, self).__init__(length=length, **kwargs)
