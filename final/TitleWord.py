import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class TitleWord(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    word = Column(Unicode(32), index = True, unique = True)

    soundex_id = Column(Integer, ForeignKey('SoundexTitleWord.id'))

    def __init__(self, session, word):
        self.word = word
        soundex_code = utils.soundexPL(word)
        soundexTitleWord = final.SoundexTitleWord.get_or_create(session, soundex_code)
        soundexTitleWord.words.append(self)

    @classmethod
    def get_or_create(cls, session, word):
        obj = SqlWrapper.get_or_create_(session, TitleWord, {"word":word, "session":session}, "word")
        session.add(obj)
        session.commit()
        return obj
