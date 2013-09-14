from sqlwrapper import *
import utils
Base = SqlWrapper.getBaseClass()

class MergeAlgorithm(Base):
    __tablename__ = "MergeAlgorithm"

    id = Column(Integer, primary_key=True)
    description = Column(Unicode(512))

    class Version(utils.Enum):
        values = ['mock', 'alpha_1', 'alpha_2', 'alpha_3']

    cache = {}
    @staticmethod
    def get_or_create(session, id):
        try:
            return MergeAlgorithm.cache[id]
        except KeyError:
            MergeAlgorithm.cache[id] = SqlWrapper.get_or_create_(session, MergeAlgorithm, {'id': id, 'description':MergeAlgorithm.Version.values[id]})
            return MergeAlgorithm.cache[id]


SqlWrapper.table_list += [MergeAlgorithm.__tablename__]

descriptions  = {
        MergeAlgorithm.Version.mock:
            """Mock algorithm - can be used for tests and development
            """,

        MergeAlgorithm.Version.alpha_1:
            """Very slow version, entirely based on Levenshtein-Length.

            Weaknesses: Levenshtein-Length (LL) is calculated always for two phrases.
            To get list of candidates this algorithm need to calculate N Levenshtein-Lengths
            only to get candidates for one MiniBook. This was very bad idea.
            """,

        MergeAlgorithm.Version.alpha_2:
            """SoundexPL-based merge algorithm. In theory it should match all books,
            which are in fact this same book. Soundex codes can be calculate only
            once per MiniBook, however can't be calculate for whole titles. Each
            title needs to be splited to seperate words, thats why new tables come
            up in this version: TitleWord, SoundexTitleWord.

            Weaknesses: it returns to much candidates, ignore simple to verify cases,
            where to books can be matched by ISBN.
            """
        ,
        MergeAlgorithm.Version.alpha_3:
            """Based on Alpha_2 alghorithm with some news:
            - Inner Merge (by ISBN)
            - multiphase, 5 steps compare algorithm
            - MiniBookCompare table, to cache results of comparing two MiniBooks
            """
        ,
    }
