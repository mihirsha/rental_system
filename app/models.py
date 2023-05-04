from app.database.database import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    books = relationship('Books', back_populates='userRented')
    cart = relationship('CartItems', back_populates='user')


association_book_author = Table(
    'association_book_author',
    Base.metadata,
    Column('book_id', ForeignKey('book.id')),
    Column('author_id', ForeignKey('author.id'))
)

association_book_genre = Table(
    'association_book_genre',
    Base.metadata,
    Column('book_id', ForeignKey('book.id')),
    Column('genre_id', ForeignKey('genre.id'))
)


class Books(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    authors = relationship(
        'Authors', secondary=association_book_author, back_populates='books')
    genres = relationship(
        'Genre', secondary=association_book_genre, back_populates='books')
    user_id = Column(Integer(), ForeignKey('user.id'))
    userRented = relationship('User', back_populates='books')
    bookDetail = relationship('BookDetails', backref='book_details')
    cart = relationship('CartItems', back_populates='book')

    def __repr__(self):
        return f"<Books {self.title}>"


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    books = relationship(
        'Books', secondary=association_book_genre, back_populates='genres')

    def __repr__(self):
        return f"<Genre {self.name}>"


class Authors(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    books = relationship(
        'Books', secondary=association_book_author, back_populates='authors')

    def __repr__(self):
        return f"<Authors {self.name}>"


class BookDetails(Base):
    __tablename__ = "book_details"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rental_price = Column(Integer, nullable=False)
    rental_period = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False)
    book_id = Column(Integer(), ForeignKey('book.id'))
    # book = relationship('Books', back_populates='bookDetail')

    def __repr__(self):
        return f"<bookDetails {self.id}>"


class CartItems(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rental_period = Column(Integer(), nullable=False)
    user_id = Column(Integer(), ForeignKey('user.id'))
    book_id = Column(Integer(), ForeignKey('book.id'))
    book = relationship('Books', back_populates='cart')
    user = relationship('user', back_populates='cart')

    def __repr__(self):
        return f"<cart_items {self.id}>"

# class Review(Base):
#     __tablename__ = "review"

#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     review = Column(String, nullable=False)
#     user_id = relationship(
#         'User', back_populates='reviews')

#     def __repr__(self):
#         return f"<Review {self.name}>"
