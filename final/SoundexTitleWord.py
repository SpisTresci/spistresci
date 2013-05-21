import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class SoundexTitleWord(final.FinalBase, Base):
    id = Column(Integer, primary_key = True)
    code = Column(Unicode(5), index = True, unique = True)

    words = relationship("TitleWord", lazy = 'joined', backref = backref("soundex", uselist = False, lazy = 'joined',))

    def __init__(self, code):
        self.code = code

    @classmethod
    def get_or_create(cls, session, code):
        obj = SqlWrapper.get_or_create_(session, SoundexTitleWord, {"code":code})
        session.add(obj)
        session.commit()
        return obj
