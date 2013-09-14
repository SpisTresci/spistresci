import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class TitleWord(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    word = Column(Unicode(32), index = True)
    soundex = Column(Integer, index = True)
    mini_book_id = Column(Integer, ForeignKey('MiniBook.id'))
    stopword = Column(Boolean)

    stopwords = None

    def __init__(self, word):
        self.word = word
        self.soundex = utils.soundexPL(word)

        if not self.stopwords:
            self.loadStopWordList()

        self.stopword = word in self.stopwords

    def loadStopWordList(self):
        with open("stopwords.txt") as sw:
            self.stopwords = []

            for line in sw:
                word = line.strip()
                if not word.startswith("#"):
                    self.stopwords.append(word)

            for i in range(0, 9):
                self.stopwords.append(str(i))

            for letter_code in range(ord('a'), ord('z')+1):
                self.stopwords.append(chr(letter_code))

