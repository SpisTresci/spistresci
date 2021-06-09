import sqlalchemy
from final import Comparable
from Levenshtein import ratio
from utils.Str import simplify
import regex


class Title(sqlalchemy.Unicode):
    class title(Comparable.Comparable, unicode):
        def cmp(self, other):
            p1 = 1.0 * ratio(self, other)
            p2 = 0.95 * ratio(self.lower(), other.lower())
            p3 = 0.8 * ratio(simplify(self), simplify(other))

            return max(p1, p2, p3)

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return Title.title(value)   # value is a regular unicode string
            else:
                return Title.title()
        return process


class Name(sqlalchemy.Unicode):

    class name(Comparable.Comparable, unicode):
        def cmp(self, other):
            r = self.Result()

            if other != None and self != "" and other != "":
                if Name.name.isInitialAndInitial(self, other):
                    r.addRatio(1.0 if self == other else 0.6)
                elif Name.name.isInitialAndName(self, other):
                    r.addRatio(0.8 if self[0] == other[0] else 0.6)
                else:
                    r.addRatio(ratio(self, other))

            return r.result()

        @staticmethod
        def isInitial(n):
            if n and n != "" and len(n) == 2 and n[1] == '.':
                m = regex.search(ur"\p{Lu}", n[0])
                if m and m.group(0) == n[0]:
                    return True
            return False

        @staticmethod
        def isInitialAndInitial(n1, n2):
            return Name.name.isInitial(n1) and Name.name.isInitial(n2)

        @staticmethod
        def isInitialAndName(n1, n2):
            return n1 and n2 and n1 != "" and n2 != "" and (Name.name.isInitial(n1) and not Name.name.isInitial(n2)) or (not Name.name.isInitial(n1) and Name.name.isInitial(n2))

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return Name.name(value)   # value is a regular unicode string
            else:
                return Name.name()
        return process



class LastName(sqlalchemy.Unicode):

    class lastname(Comparable.Comparable, unicode):

        def cmp(self, other):
            r = self.Result()

            if other != None:
                r.addRatio(ratio(self, other))

            return r.result()

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return LastName.lastname(value)   # value is a regular unicode string
            else:
                return LastName.lastname()
        return process
