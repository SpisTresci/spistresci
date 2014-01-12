# -*- coding: utf-8 -*-
from sqlalchemy.orm import joinedload
from connectors.generic import ReferenceConnector
from models.UpdateStatusService import UpdateStatusService
import time
import utils
from sqlwrapper import *
import final
from Comparable import *

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
    session = None

    @staticmethod
    def insert(connector):
        connector.save_time_of_("final_start")
        if isinstance(connector, ReferenceConnector):
            Final.insertReferenceConnectorData(connector)
        else:
            Final.insertSpecificConnectorData(connector)
        connector.session.commit()
        connector.save_time_of_("final_end")

    @staticmethod
    def insertSpecificConnectorData(connector):
        session = connector.session

        SpecificBook = connector.getConcretizedClass(connector, "Book")
        new_specific_books = session.query(SpecificBook).filter(SpecificBook.mini_book_id == None).all()
        i = 0
        for specific_book in new_specific_books:
            mini_book = final.MiniBook(session, specific_book)
            session.add(mini_book)

            i += 1
            print str(i)
            if i % 1000 == 0: session.commit()

        last_final = session.query(UpdateStatusService).filter(UpdateStatusService.service_name == connector.name, UpdateStatusService.final_end != None).order_by(UpdateStatusService.final_end.desc()).first()

        if last_final:
            last_final_timestamp = time.mktime(last_final.final_start.timetuple())
            updated_specific_books = session.query(SpecificBook).filter(SpecificBook.update_minidata_timestamp > last_final_timestamp).all()
        else:
            updated_specific_books = session.query(SpecificBook).all()

        i = 0
        for specific_book in updated_specific_books:
            mini_book = SqlWrapper.get_(session, final.MiniBook, {"id":SpecificBook.mini_book_id})
            mini_book.update(session, specific_book)
            i += 1
            print "Price update: " + str(i)
            if i % 1000 == 0: session.commit()

        session.commit()
        session.close()

    @staticmethod
    def mergeFromBigOrderedQuery(minibooks, atr_extractor):
        last = ''
        to_merge = []
        for mini in minibooks:
            if last != atr_extractor(mini):
                last = atr_extractor(mini)
                master_books = [m.master for m in to_merge[1:]]
                if len(to_merge) > 0:
                    to_merge[0].master.cmp_with_list(master_books)
                to_merge=[mini]
            else:
                to_merge.append(mini)

            #print '[' + str(mini.master_id) + ']' + mini.title

    @staticmethod
    def mergeByISBN(connector, inner_merge=False):
        if connector:
            minis = connector.session.query(final.MiniBook).filter(final.MiniBook.bookstore == connector.name).all()
            for mini in minis:
                master_books = mini.getMasterBooksCandidatesByISBN(connector.session, mini.master.isbn, inner_merge)
                mini.master.cmp_with_list(master_books)
        else:#  Optimized version for all connector at once
            subq = Final.session.query(final.MiniISBN, func.count()).group_by(final.MiniISBN.core).having(func.count()>1).subquery()
            subq2 = Final.session.query(final.MiniISBN).join(subq, subq.c.core == final.MiniISBN.core).order_by(subq.c.core).subquery()
            minibooks = Final.session.query(final.MiniBook).join(subq2, subq2.c.mini_book_id == final.MiniBook.id).order_by(subq2.c.core).all()

            Final.mergeFromBigOrderedQuery(minibooks, lambda mini: mini.isbns[0].core)
            """
            last_isbn = ''
            to_merge = []
            for mini in minibooks:
                if last_isbn != mini.isbns[0].core:
                    last_isbn = mini.isbns[0].core
                    master_books = [m.master for m in to_merge[1:]]
                    if len(to_merge) > 0:
                        to_merge[0].master.cmp_with_list(master_books)
                    to_merge=[mini]
                else:
                    to_merge.append(mini)
            """
        Final.session.commit()

    @staticmethod
    def mergeByTitle(connector):
        if connector:
            minis = connector.session.query(final.MiniBook).filter(final.MiniBook.bookstore == connector.name).all()
            for mini in minis:
                master_books = mini.getMasterBooksCandidatesByTitle(connector.session, mini.master.title)
                mini.master.cmp_with_list(master_books)
        else:#  Optimized version for all connector at once
            subq = Final.session.query(final.MiniBook, func.count()).group_by(final.MiniBook.title).having(func.count()>1).subquery()
            minibooks = Final.session.query(final.MiniBook).join(subq, subq.c.title == final.MiniBook.title).order_by(final.MiniBook.title).all()

            Final.mergeFromBigOrderedQuery(minibooks, lambda mini: mini.title)

        Final.session.commit()


    @staticmethod
    def inner_merge(connector):
        Final.session = connector.session

        #minis = Final.session.query(final.MiniBook).options(joinedload('isbns')).filter(final.MiniBook.bookstore == connector.name).all()
        minis = Final.session.query(final.MiniBook).options(joinedload('words')).filter(final.MiniBook.bookstore == connector.name).all()
        #minis = Final.session.query(final.MiniBook).filter(final.MiniBook.bookstore == connector.name).all()

        i = 0
        no_of_candidates = []
        no_of_words = []
        no_of_stop_words = []
        for mini in minis:

            #candidates = mini.getCandidatesByISBN(connector.session, inner=True)
            candidates = mini.getCandidatesByTitleWord(connector.session, inner=True)
            print "inner_merge_mini: " + str(i) + ", len(candidates): " + str(len(candidates))

            no_st = len([word for word in mini.words if word.stopword])
            no_of_words.append(len(mini.words)-no_st)
            no_of_stop_words.append(no_st)


            for candidate in candidates:
                #print "inner_merge_mini: " + str(i) + "\t" + str(j)
                cmp(mini, candidate)

            no_of_candidates.append(len(candidates))
            i += 1

            if i % 1000== 0:
                print str(i)
                print "Srednia liczba kandydatow: " + str(sum(no_of_candidates)/float(len(no_of_candidates)))
                print "Mediana liczby kandydatow: " + str(sorted(no_of_candidates)[len(no_of_candidates)/2])

                print "Srednia liczba słów w tytule: " + str(sum(no_of_words)/float(len(no_of_words)))
                print "Mediana liczby słów w tytule: " + str(sorted(no_of_words)[len(no_of_words)/2])

                print "Srednia liczba stopsłów w tytule: " + str(sum(no_of_stop_words)/float(len(no_of_stop_words)))
                print "Mediana liczby stopsłów w tytule: " + str(sorted(no_of_stop_words)[len(no_of_stop_words)/2])

                Final.session.commit()


        Final.session.commit()

    @staticmethod
    def merge(connector):
        Final.mergeByISBN(connector)

class FinalBase(object):
    @declared_attr
    def __tablename__(cls):
        SqlWrapper.table_list.append(cls.__name__)
        return cls.__name__
