from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database.database import get_db
from app.models import Authors, Books
from app.utils import hash, validMobileNumber
from app.schemas import Book, BookOut


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
        print(newBook.authors)
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
