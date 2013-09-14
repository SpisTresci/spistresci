from sqlwrapper import *

Base = SqlWrapper.getBaseClass()

class Service(Base):
    __tablename__ = "Service"

    name = Column(Unicode(32), primary_key=True)
    website = Column(Unicode(32))
    #path_to_logo
    #facebook
    #google_plus
    #twitter

    @classmethod
    def get_or_create(cls, connector, session = None):
        if not session:
            session = SqlWrapper.scoped_session()

        service = session.query(Service).filter_by(name = connector.name).first()

        if service:
            return service
        else:
            service = Service(connector)
            session.add(service)
            session.commit()
            return service


    def __init__(self, connector):
        self.name = connector.name
        self.website = u"#"   #TODO: add reading info from additional config

    def load_from_config(self):
        pass

SqlWrapper.table_list += [Service.__tablename__]



"""
from sqlwrapper import *
import utils
Base = SqlWrapper.getBaseClass()

class BookType(Base):
    __tablename__ = "BookType"

    class BookType(utils.Enum):
        #enums starts from 0, id can start from 1, so first (0) enum cannot be used.
        values = ['DO_NOT_USE', 'NOINFO', 'HYBRID', 'EBOOK', 'AUDIOBOOK', 'BOOK', 'PRESS']

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(16))

    cache = {}
    @staticmethod
    def get_or_create(session, id):
        try:
            return BookType.cache[id]
        except KeyError:
            BookType.cache[id] = SqlWrapper.get_or_create_(session, BookType, {'id': id, 'name':BookType.BookType.values[id]})
            session.add(BookType.cache[id])
            return BookType.cache[id]

    @staticmethod
    def fromFormats(format_list):
        if len(format_list) == 0:
            return BookType.BookType.NOINFO

        types = []
        for type, formats in book_types.items():
            for format in format_list:
                if format in formats:
                    types.append(type)
                    break

        return types[0] if len(types) == 1 else BookType.BookType.HYBRID


SqlWrapper.table_list += [BookType.__tablename__]

book_types  = {
        #0 - BookType.BookType.DO_NOT_USE:[],
        BookType.BookType.NOINFO:['dvd', 'unknown'],
        BookType.BookType.HYBRID:[],
        BookType.BookType.EBOOK:['epub', 'mobi', 'pdf', 'txt', 'xml', 'fb2', 'pdf_drm', 'online', 'ebook_unknown'],
        BookType.BookType.AUDIOBOOK:['cd', 'cd_mp3', 'mp3', 'online_audio', 'audiobook_unknown'],
        BookType.BookType.BOOK:['ks'],
        BookType.BookType.PRESS:['press_mobi', 'press_epub', 'press_pdf', 'press_online'],
    }
"""