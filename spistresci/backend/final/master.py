from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

master_books_master_authors = Table('master_books_master_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('MasterBook.id')),
    Column('author_id', Integer, ForeignKey('MasterAuthor.id'))
)
SqlWrapper.table_list.append('master_books_master_authors')

#master_books_master_isbns = Table('master_books_master_isbns', Base.metadata,
#    Column('book_id', Integer, ForeignKey('MasterBook.id')),
#    Column('isbn_id', Integer, ForeignKey('MasterISBN.id'))
#)
#SqlWrapper.table_list.append('master_books_master_isbns')

master_books_title_words = Table('master_books_title_words', Base.metadata,
    Column('book_id', Integer, ForeignKey('MasterBook.id')),
    Column('title_id', Integer, ForeignKey('TitleWord.id'))
)
SqlWrapper.table_list.append('master_books_title_words')
