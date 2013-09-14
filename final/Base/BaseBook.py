from final.Final import FinalBase
from ..Comparable import *
from final.FinalTypes import Title

class BaseBook(Comparable, FinalBase):
    id = Column(Integer, primary_key = True)

    title = Column(Title(512))
    cover = Column(Unicode(512), nullable = False)
    price = Column(Integer, nullable = False)

    @declared_attr
    def description_id(cls):
        return Column(Integer, ForeignKey('BookDescription.id'))

    @declared_attr
    def description(cls):
        return relationship("BookDescription", uselist=False)

    #supported_formats = ['cd', 'cd-mp3', 'dvd', 'epub', 'fb2', 'ks', 'mobi', 'mp3', 'pdf', 'txt', 'xml']
    format_cd = Column(Boolean, default=False)
    format_cd_mp3 = Column(Boolean, default=False)
    format_dvd = Column(Boolean, default=False)
    format_epub = Column(Boolean, default=False)
    format_fb2 = Column(Boolean, default=False)
    format_ks = Column(Boolean, default=False)
    format_mobi = Column(Boolean, default=False)
    format_mp3 = Column(Boolean, default=False)
    format_pdf = Column(Boolean, default=False)
    format_txt = Column(Boolean, default=False)
    format_xml = Column(Boolean, default=False)

