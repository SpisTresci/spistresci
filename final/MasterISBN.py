import final
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class MasterISBN(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)

    raw = Column(Unicode(50))
    #raw_simplified = Column(STUnicode(50))
    core = Column(STUnicode(9))
    isbn10 = Column(Unicode(10))
    isbn13 = Column(Unicode(13))
    valid = Column(Boolean)

    miniISBNs = relationship("MiniISBN", backref = backref("masterISBN", uselist = False))

    def __init__(self, mini_isbn):
        if not isinstance(mini_isbn, final.MiniISBN):
            raise Exception("MasterISBN can be initialized only by MiniISBN")

        self.raw = mini_isbn.raw
        #self.raw_simplified = mini_isbn.raw_simplified
        self.core = mini_isbn.core
        self.isbn10 = mini_isbn.isbn10
        self.isbn13 = mini_isbn.isbn13
        self.valid = mini_isbn.valid
