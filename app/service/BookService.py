from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database.database import get_db
from app.models import Authors, Books, User
from app.utils import hash, validMobileNumber
from app.schemas import Book, BookOut, updateBookUser


class BookService:

    def addBook(reqbook: Book, db: Session):
        authorsList = []
        book = db.query(Books).filter(reqbook.title == Books.title).first()
        if book is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book with title *{reqbook.title}* already exists")

        for i in range(len(reqbook.authors)):
            author: Authors = db.query(Authors).filter(
                reqbook.authors[i] == Authors.id).first()

            if author is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"author with id {reqbook.authors[i]} already exists")
            else:
                authorsList.append(author)

        newBook = Books(
            title=reqbook.title,
            description=reqbook.description,
            authors=authorsList
        )
        db.add(newBook)
        db.commit()
        db.refresh(newBook)

        return BookOut(
            title=newBook.title,
            description=newBook.description,
            authors=newBook.authors
        )

    def getBooks(bookName: str, db: Session):
        book = db.query(Books).filter(bookName == Books.title).first()
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book with title *{bookName}* does not exists")

        else:
            return book

    def updateBookUser(req: updateBookUser, db: Session):
        book: Books = db.query(Books).filter(Books.id == req.book_id).first()
        user: User = db.query(User).filter(User.id == req.user_id).first()
        if user == None and req.user_id != -1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id *{req.user_id}* does not exists")
        if book == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id *{req.book_id}* does not exists")

        if req.user_id == -1:
            book.user_id = None
            db.add(book)
            db.commit()
            db.refresh(book)
        else:
            book.user_id = user.id
            db.add(book)
            db.commit()
            db.refresh(book)
        return book

    def deleteBook(book_id: int, db: Session):
        book = db.query(Books).filter(Books.id == book_id).first()
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id *{book_id}* does not exists")

        db.delete(book)
        db.commit()

        return f'Deleted Bookid {book_id}'
