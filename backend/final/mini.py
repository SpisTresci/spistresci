from sqlwrapper import *
Base = SqlWrapper.getBaseClass()

mini_books_mini_authors = Table('mini_books_mini_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('MiniBook.id')),
    Column('author_id', Integer, ForeignKey('MiniAuthor.id'))
)
SqlWrapper.table_list.append('mini_books_mini_authors')

mini_books_mini_isbns = Table('mini_books_mini_isbns', Base.metadata,
    Column('book_id', Integer, ForeignKey('MiniBook.id')),
    Column('isbn_id', Integer, ForeignKey('MiniISBN.id'))
)
SqlWrapper.table_list.append('mini_books_mini_isbns')


#mini_books_title_words = Table('mini_books_title_words', Base.metadata,
#    Column('book_id', Integer, ForeignKey('MiniBook.id')),
#    Column('title_id', Integer, ForeignKey('TitleWord.id'))
#)
#SqlWrapper.table_list.append('mini_books_title_words')
