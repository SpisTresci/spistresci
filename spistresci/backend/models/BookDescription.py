from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

class BookDescription(Base):
    __tablename__ = 'BookDescription'

    id = Column(Integer, primary_key=True)
    description = Column(Unicode(20000)) #TODO: parametr musi byc dynamicznie ustawiany

    def __unicode__(self):
        return unicode(self.description)

    def __init__(self, initial_data):
        try:
            self.description = initial_data['description']
        except:
            exit('Record ' + initial_data + ' doesn\'t have defined desription')

SqlWrapper.table_list += [BookDescription.__tablename__]