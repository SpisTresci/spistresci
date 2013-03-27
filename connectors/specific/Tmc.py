from afiliant import *
from sql_wrapper import *

Base = SqlWrapper.getBaseClass()

class Tmc(Afiliant):
    def parse(self):
        pass

class TmcBook(AfiliantBook, Base):
    pass

class TmcBookDescription(AfiliantBookDescription, Base):
    pass

class TmcAuthor(AfiliantAuthor, Base):
    pass

class TmcBookPrice(AfiliantBookPrice, Base):
    pass

class TmcBooksAuthors(AfiliantBooksAuthors, Base):
    pass