from Levenshtein import ratio, distance
from utils.DataValidator import DataValidator
import final
from unidecode import unidecode

class SimilarityCalculator():

    accept_threshold = 0.85

    ############# AUTHORS ##################
    @staticmethod
    def eq_authors(a1, a2, accept_threshold = None):
        if not accept_threshold:
            accept_threshold = SimilarityCalculator.accept_threshold

        p = SimilarityCalculator.authors_ratio(a1, a2)
        """
        print ""
        if p == 1.0:
            print u"SC_AUTH:         <" + a1.name + u">"
            print u"SC_AUTH:    ==   <" + a2.name + u">   [" + str(p) + u"]"
        elif p >= accept_threshold:
            print u"SC_AUTH:         <" + a1.name + u">"
            print u"SC_AUTH:   ~==   <" + a2.name + u">   [" + str(p) + u"]"
        else:
            print u"SC_AUTH:         <" + a1.name + u">"
            print u"SC_AUTH:    !=   <" + a2.name + u">   [" + str(p) + u"]"
        """
        # p = SimilarityCalculator.authors_ratio(a1, a2)
        return  p >= accept_threshold

    @staticmethod
    def authors_ratio(a1, a2):

        h = SimilarityCalculator.Helper()
        if a1.name == a2.name:
            return 1.0
        else:
            SimilarityCalculator.lastName(h, a1.lastName, a2.lastName)
            SimilarityCalculator.firstName(h, a1.firstName, a2.firstName)
            SimilarityCalculator.middleName(h, a1.middleName, a2.middleName)

            return max(h.result(), ratio(a1.name, a2.name) * 0.8)

    @staticmethod
    def lastName(h, n1, n2):
        if n1 != None and n2 != None:
            h.add(ratio(n1, n2))

    @staticmethod
    def firstOrMiddleName(h, n1, n2):
        if n1 != None and n2 != None and n1 != "" and n2 != "":
            if SimilarityCalculator.isInitialAndInitial(n1, n2):
                h.add(1.0 if n1 == n2 else 0.6)
            elif SimilarityCalculator.isInitialAndName(n1, n2):
                h.add(0.8 if n1[0] == n2[0] else 0.6)
            else:
                h.add(ratio(n1, n2))

    @staticmethod
    def firstName(h, n1, n2):
        SimilarityCalculator.firstOrMiddleName(h, n1, n2)

    @staticmethod
    def middleName(h, n1, n2):
        SimilarityCalculator.firstOrMiddleName(h, n1, n2)

    @staticmethod
    def isInitial(n):
        import regex
        if n and n != "" and len(n) == 2 and n[1] == '.':
            m = regex.search(ur"\p{Lu}", n[0])
            if m and m.group(0) == n[0]:
                return True

        return False

    @staticmethod
    def isInitialAndInitial(n1, n2):
        return SimilarityCalculator.isInitial(n1) and SimilarityCalculator.isInitial(n2)

    @staticmethod
    def isInitialAndName(n1, n2):
        return n1 and n2 and n1 != "" and n2 != "" and (SimilarityCalculator.isInitial(n1) and not SimilarityCalculator.isInitial(n2)) or (not SimilarityCalculator.isInitial(n1) and SimilarityCalculator.isInitial(n2))

    ############# ISBNS ##################
    @staticmethod
    def eq_isbns(a1, a2, accept_threshold = None):
        if not accept_threshold:
            accept_threshold = SimilarityCalculator.accept_threshold

        p = SimilarityCalculator.isbns_ratio(a1, a2)
        """
        print ""
        if p == 1.0:
            print u"SC_ISBNS:        <" + a1.raw + u">"
            print u"SC_ISBNS:   ==   <" + a2.raw + u">   [" + str(p) + u"]"
        elif p >= accept_threshold:
            print u"SC_ISBNS:        <" + a1.raw + u">"
            print u"SC_ISBNS:  ~==   <" + a2.raw + u">   [" + str(p) + u"]"
        else:
            print u"SC_ISBNS:        <" + a1.raw + u">"
            print u"SC_ISBNS:   !=   <" + a2.raw + u">   [" + str(p) + u"]"
        """
        return  p >= accept_threshold

    @staticmethod
    def isbns_ratio(i1, i2):
        h = SimilarityCalculator.Helper()
        if i1.raw == i2.raw and i1.valid:
            h.add(1.0)
        else:
            if i1.isbn10 == i2.isbn10 and i1.valid:
                h.add(1.0)
            elif i1.isbn13 == i2.isbn13 and i1.valid:
                h.add(1.0)
            elif i1.core == i2.core and i1.valid:
                h.add(0.95)
            elif i1.raw == i2.raw and not i1.valid:
                h.add(0.9)
            elif (not i1.valid and i2.valid) or (i1.valid and not i2.valid):
                i1_ = SimilarityCalculator.simplify(i1.raw).replace("-", "")
                i2_ = SimilarityCalculator.simplify(i2.raw).replace("-", "")

                if distance(i1_, i2_) == 1:
                    if i1_[:-1] == i2_[:-1]:  # checksum is different
                        h.add(0.85)
                    else:
                        h.add(0.75)
                elif distance(i1_, i2_) == 2:
                    h.add(0.70)

        return h.result()

    ############# TITLES ##################
    @staticmethod
    def eq_titles(b1, b2, accept_threshold = None):
        if not accept_threshold:
            accept_threshold = SimilarityCalculator.accept_threshold

        p = SimilarityCalculator.titles_ratio(b1, b2)
        """
        if p == 1.0:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:   ==   <" + b2.title + u">   [" + str(p) + u"] \n"
        elif p >= accept_threshold:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:  ~==   <" + b2.title + u">   [" + str(p) + u"] \n"
        else:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:   !=   <" + b2.title + u">   [" + str(p) + u"] \n"
        """
        return  p >= accept_threshold

    @staticmethod
    def titles_ratio(t1, t2):
        p1 = 1.0 * ratio(t1, t2)
        p2 = 0.95 * ratio(t1.lower(), t2.lower())
        p3 = 0.8 * ratio(SimilarityCalculator.simplify(t1), SimilarityCalculator.simplify(t2))

        return max(p1, p2, p3)

    ############# BOOKS ##################
    @staticmethod
    def eq_books(b1, b2, accept_threshold = None):
        if not accept_threshold:
            accept_threshold = SimilarityCalculator.accept_threshold

        p = SimilarityCalculator.mini_master_books_ratio(b1, b2)
        """
        if p == 1.0:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:   ==   <" + b2.title + u">   [" + str(p) + u"] \n"
        elif p >= accept_threshold:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:  ~==   <" + b2.title + u">   [" + str(p) + u"] \n"
        else:
            print u"SC_TITLE:        <" + b1.title + u">"
            print u"SC_TITLE:   !=   <" + b2.title + u">   [" + str(p) + u"] \n"
        """
        return  p >= accept_threshold


    @staticmethod
    def mini_master_books_ratio(mini_book, master_book):
        if not (isinstance(mini_book, final.MiniBook) and isinstance(master_book, final.MasterBook)):
            raise Exception("mini_master_books_ratio - wrong argument")

        h = SimilarityCalculator.Helper()
        h.add(SimilarityCalculator.titles_ratio(mini_book.title, master_book.title))

        # if len(mini_book.authors) > 0 and len(master_book.authors) > 0:
        matched_authors = mini_MA_len = master_MA_len = 0
        for mini_MA in mini_book.authors:
            mini_MA_len += 1
            for master_MA in master_book.authors:
                master_MA_len += 1
                if mini_MA.master_id == master_MA.id:
                    matched_authors += 1

        if min(mini_MA_len, master_MA_len) > 0:
            p = matched_authors / float(min(mini_MA_len, master_MA))
            h.add(p)

        # if len(mini_book.isbns) > 0 and len(master_book.isbns) > 0:
        matched_isbns = mini_MI_len = master_MI_len = 0
        for mini_MI in mini_book.isbns:
            mini_MI_len += 1
            for master_MI in master_book.isbns:
                master_MI_len += 1
                if mini_MI.master_id == master_MI.id:
                    matched_isbns += 1

        if min(mini_MI_len, master_MI_len) > 0:
            p = matched_isbns / float(min(mini_MI_len, master_MI_len))
            h.add(p)

        return h.result()

    ########### OTHER TOOLS ##################

    @staticmethod
    def removeDiacritics(t):
        return unidecode(t)

    @staticmethod
    def simplify(s):
        return SimilarityCalculator.removeDiacritics(DataValidator().simplifyHyphens(s).lower())

    class Helper():
        def __init__(self):
            self.tests = []

        def add(self, ratio):
            self.tests.append(ratio)

        def result(self):
            #return self.avg(self.tests)
            return self.geo_avg(self.tests)

        def geo_avg(self, tests):
            if len(tests) == 0:
                return 0.0

            r = 1.0
            for t in tests:
                r *= t
            return r ** (1.0 / len(tests))

        def avg(self, tests):
            if len(tests) == 0:
                return 0.0

            return sum(tests) / float(len(tests))
