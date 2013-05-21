from connectors.generic import ReferenceConnector
import utils
from sqlwrapper import *
import final

#######################################################################################
#          Master          #            Mini              #          Specific         #
#######################################################################################
#  MasterBook              #  MiniBook                    #  LegimiBook               #
#  MasterISBN              #  MiniISBN                    #  LegimiAuthor             #
#  MasterAuthor            #  MiniAuthor                  #  LegimiFormat             #
#                          #                              #  LegimiISBN               #
#                          #                              #  ....                     #
#                          #                              #  ....                     #
#                          #                              #  NextoBook                #
#                          #                              #  NextoAuthor              #
#                          #                              #  NextoFormat              #
#                          #                              #  ....                     #
#######################################################################################

class Final(object):

    def insert(self, connector):
        if isinstance(connector, ReferenceConnector):
            self.insertReferenceConnectorData(connector)
        else:
            self.insertSpecificConnectorData(connector)

    @staticmethod
    def addNormalizeList(session, flush_context):
        for new in session.new:
            if isinstance(new, (final.MiniBook, final.MiniAuthor, final.MiniISBN)):
                new.to_normalize.append(new)

    def insertSpecificConnectorData(self, connector):
        Session = sessionmaker(bind = SqlWrapper.getEngine())
        session = Session()
        from sqlalchemy import event
        event.listen(Session, "after_flush", self.addNormalizeList)

        specific_books = session.query(connector.getConcretizedClass(connector, "Book")).all()
        for specific_book in specific_books:
            mini_book = final.MiniBook(session, specific_book)
            session.add(mini_book)
            session.commit()
            final.MiniBook.normalize(session)

        session.commit()
        session.close()

    def addToMasterBook(self, session, mini_book, master_book):
        master_book.mini_book.append(mini_book)
        session.add(master_book)
        session.commit()

    def matchSpecificBookWithMasterBooks(self, session, specific_book, master_books):
        matched = []
        for master_book in master_books:

            #if all(any(eq_authors(specific_author, master_author) for master_author in master_book.authors) for specific_author in specific_book.authors) and
            #all(any(eq_authors(master_author, specific_author) for specific_author in specific_book.authors) for master_author in master_book.authors):
            #    pass

            m_as = list(master_book.authors)
            s_as = list(specific_book.authors)

            authors_are_equal = True
            for ma, sa in zip(sorted(m_as), sorted(s_as)):
                if not utils.SimilarityCalculator.eq_authors(ma, sa):
                    authors_are_equal = False

            isbns_are_equal = True
            #len(list(master_book.isbns)) == len(list(specific_book.isbns)) and
            for mi, si in zip(sorted(master_book.isbns), sorted(specific_book.isbns)):
                if not utils.SimilarityCalculator.eq_isbns(si, mi):
                    isbns_are_equal


            titles_are_equal = utils.SimilarityCalculator.eq_titles(master_book.title, specific_book.title)

            if authors_are_equal and isbns_are_equal and titles_are_equal: #super easy case!
                matched.append(master_book)

        return matched

    def getMasterBooksCandidates(self, session, specific_book):
        r = []

        #EXACT ISBN
        for isbn in specific_book.isbns:
            r.append([mi.master_book for mi in session.query(final.MasterISBN).filter_by(core = isbn.core).all()])

        #TODO: add support for:
        #Similar ISBN, levenstain() <= 2


        #EXACT TITLE
        r.append(session.query(final.MasterBook).filter_by(title = specific_book.title).all())

        #final.MasterBook.title cointains specific_book.title

        r.append(session.query(final.MasterBook).filter(final.MasterBook.title.contains(specific_book.title)).all())
        #specific_book.title cointainsfinal.MasterBook.title
        r.append(session.query(final.MasterBook).filter(bindparam('btitle', specific_book.title).contains(final.MasterBook.title)).all())

        #union on all lists in the list 'r'
        result = []
        for list_elem in r:
            result = list(set(result) | set(list_elem))

        return result



class FinalBase(object):
    @declared_attr
    def __tablename__(cls):
        SqlWrapper.table_list.append(cls.__name__)
        return cls.__name__
