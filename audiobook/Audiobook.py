from afiliant import *
from sql_wrapper import *

Base = SqlWrapper.getBaseClass()

class Audiobook(Afiliant):
    pass

class AudiobookBook(AfiliantBook, Base):
    id =  Column(Integer, primary_key=True)

    category = Column(Unicode(25))      #21
    #title(255)                         #122
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(1))         #0

class AudiobookBookDescription(AfiliantBookDescription, Base):
    pass

class AudiobookAuthor(AfiliantAuthor, Base):
    pass

class AudiobookBookPrice(AfiliantBookPrice, Base):
    pass

class AudiobookBooksAuthors(AfiliantBooksAuthors, Base):
    pass