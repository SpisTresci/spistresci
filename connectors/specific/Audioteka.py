from connectors.common import *
from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Audioteka(Afiliant):
    def validate(self, dic):
        Afiliant.validate(self, dic)

        id=dic.get('external_id')
        title=dic.get('title')
        self.validateAuthors(dic, id, title, 'lectors')

class AudiotekaBook(AfiliantBook, Base):
    id =  Column(Integer, primary_key=True)

    category = Column(Unicode(25))      #21
    publisher = Column(Unicode(70))     #57
    #title(255)                         #122
    #description                        #0
    url = Column(Unicode(70))           #60
    price = Column(Integer)             #GROSZE!!!
    cover = Column(Unicode(150))        #145
    length = Column(Unicode(20))        #16
    #lectors
    external_id = Column(Unicode(90), unique=True) #86

class AudiotekaBookDescription(AfiliantBookDescription, Base):
    pass

class AudiotekaAuthor(AfiliantAuthor, Base):
    pass

class AudiotekaBookPrice(AfiliantBookPrice, Base):
    pass

class AudiotekaBooksAuthors(AfiliantBooksAuthors, Base):
    pass