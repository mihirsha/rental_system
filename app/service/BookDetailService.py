from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import BookDetails, Books
from app.schema.BookDetailSchema import BookDetailInput, BookResponse


class BookDetailService:

    def addBookDetails(request: BookDetailInput, db: Session):
        bookFetch = db.query(Books).filter(
            request.book_id == Books.id).first()
        bookDetailFetch = db.query(BookDetails).filter(
            request.book_id == BookDetails.book_id).first()
        if bookDetailFetch is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book details for bookid {request.book_id} already exists")
        if bookFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book does not exist")
        else:
            newBookDetails = BookDetails(
                book_id=request.book_id,
                rental_price=request.rental_price,
                rental_period=request.rental_period,
                availability=request.availability
            )

            db.add(newBookDetails)
            db.commit()
            db.refresh(newBookDetails)

        return newBookDetails

    def getBookDetails(book_id: int, db: Session):
        bookFetch = db.query(Books).filter(book_id == Books.id).first()
        bookDetailFetch = db.query(BookDetails).filter(
            book_id == BookDetails.book_id).first()
        if bookFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book not found")
        if bookDetailFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book details for book {book_id} not available")

        return bookFetch

    def deleteBookDetail(book_id: int, db: Session):
        bookDetailFetch = db.query(BookDetails).filter(
            book_id == BookDetails.book_id).first()
        if bookDetailFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book details for bookid {book_id} does not exists")
        else:
            db.delete(bookDetailFetch)
            db.commit()
        return f"deleted book details for id *{book_id}*"
