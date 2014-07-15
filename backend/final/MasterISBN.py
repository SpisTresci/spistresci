import final
from sqlwrapper import *
from Comparable import *
from final.Base.BaseISBN import *
from final.Base.BaseMaster import *

Base = SqlWrapper.getBaseClass()

class MasterISBN(BaseMaster, BaseISBN, Base):
    book_id = Column(Integer, ForeignKey('MasterBook.id'))
    minis = relationship("MiniISBN", backref = backref("master", uselist = False))

    def __init__(self, mini_isbn):
        if not isinstance(mini_isbn, final.MiniISBN):
            raise Exception("MasterISBN can be initialized only by MiniISBN")

        self.raw = mini_isbn.raw
        #self.raw_simplified = mini_isbn.raw_simplified
        self.core = mini_isbn.core
        self.isbn10 = mini_isbn.isbn10
        self.isbn13 = mini_isbn.isbn13
        self.valid = mini_isbn.valid

    def __repr__(self):
        return "[%d](%s)%s" % (self.id, ", ".join([str(mini.id) for mini in self.minis]), self.raw)

    #########################

    def addMini(self, other):
        pass

    def removeMini(self, other):
        pass
