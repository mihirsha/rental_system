from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import Authors, Books, User, Genre
from app.schema.BookSchema import Book, updateBookUser
import shutil
import uuid
# Printing random id using uuid1()


class BookService:

    async def addBook(reqbook: Book, db: Session, file):

        authorsList = []
        genreList = []
        book = db.query(Books).filter(reqbook.title == Books.title).first()
        if book is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book with title *{reqbook.title}* already exists")

        for i in range(len(reqbook.authors)):
            author: Authors = db.query(Authors).filter(
                reqbook.authors[i] == Authors.id).first()

            if author is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"author with id {reqbook.authors[i]} does not exists")
            else:
                authorsList.append(author)

        for i in range(len(reqbook.genres)):
            genre: Genre = db.query(Genre).filter(
                reqbook.genres[i] == Genre.id).first()

            if genre is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Genre with id {reqbook.authors[i]} does not exists")
            else:
                genreList.append(genre)

        uuids = uuid.uuid1()
        newBook = Books(
            id=uuids,
            title=reqbook.title,
            description=reqbook.description,
            authors=authorsList,
            genres=genreList
        )

        db.add(newBook)
        db.commit()
        db.refresh(newBook)

        file.filename = f"{uuids}.pdf"
        print(file.filename)
        contents = await file.read()
        workdir = "books_pdf_DB/"
        with open(f"{workdir}{file.filename}", "wb") as f:
            f.write(contents)

        return newBook

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
