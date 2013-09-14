import final
import utils
from sqlwrapper import *
Base = SqlWrapper.getBaseClass()
"""
class SoundexTitleWord(final.FinalBase, Base):
    code = Column(Integer, primary_key = True, index = True)#, unique = True)

    @declared_attr
    def words(cls):
        if SqlWrapper.isEgoistStrategyOn():
            return relationship("TitleWord", lazy = 'joined',               backref = backref("soundex", uselist = False, lazy = 'joined'))
        else:
            return relationship("TitleWord", lazy = 'joined', cascade = "", backref = backref("soundex", uselist = False, lazy = 'joined'))

    def __init__(self, code):
        self.code = code

    @classmethod
    def get_or_create(cls, session, code):
        obj = SqlWrapper.create_(session, SoundexTitleWord, {"code":code})
        session.add(obj)

        if not SqlWrapper.isEgoistStrategyOn():
            session.commit()

        return obj
"""