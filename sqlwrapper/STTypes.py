import sqlalchemy


class STUnicode(sqlalchemy.Unicode):
    class comparator_factory(sqlalchemy.Unicode.Comparator):
        def isSimilar(self, other):
            return sqlalchemy.sql.func.levenshtein(self.expr, other) < 4

class STUnicode10(sqlalchemy.Unicode):
    class comparator_factory(sqlalchemy.Unicode.Comparator):
        def isSimilar(self, other):
            return sqlalchemy.sql.func.levenshtein(self.expr, other) < 10