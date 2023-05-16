from sqlalchemy.orm import Session
from sqlalchemy import delete
from fastapi import status, HTTPException
from app.models import Books, BookDetails, CartItems, User
from app.schema.PaymentSchema import PaymentInput
from datetime import datetime, timedelta
from app.utils import send_email


class PaymentService:

    def paymentAdd(email: str, db: Session):
        """
            -> check bookDetail availability is True
            -> bookDetail availability turn false
            -> updating user id in book table
            -> clear cart

        """
        # expire = datetime.utcnow() + timedelta(days=)

        user = db.query(User).filter(User.email == email).first()
        bookFetch = db.query(CartItems).filter(
            CartItems.user_id == user.id).all()

        if bookFetch == []:
            raise HTTPException(
                status_code=status.HTTP_200_OK, detail=f"No Books in cart to be checkedout")

        for book in bookFetch:
            bookDetail = db.query(BookDetails).filter(
                BookDetails.book_id == book.book_id).first()
            if bookDetail is None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book detail for book id {book.book_id} not available")

            if bookDetail.availability == False:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Book with id {book.book_id} is already taken kindly delete it from your cart")

        for book in bookFetch:

            singleBook = db.query(Books).filter(
                Books.id == book.book_id).first()
            singleBook.bookDetail.availability = False
            singleBook.bookDetail.rented_day = datetime.utcnow()
            singleBook.bookDetail.release_day = datetime.utcnow() + \
                timedelta(days=book.rental_period)
            singleBook.user_id = user.id

            details = db.query(BookDetails).filter(
                BookDetails.book_id == book.book_id).first()
            details.rented_day = datetime.utcnow()
            details.release_day = datetime.utcnow() + timedelta(days=book.rental_period)
            details.availability = False
            db.add(singleBook)
            db.commit()

            db.add(details)
            db.commit()

        items = db.query(CartItems).filter(CartItems.user_id == user.id).all()
        items_string = ""
        for item in items:
            items_string += f"\n * {item.books.title}"
            db.delete(item)
            db.commit()

        send_email(
            user.email, f"Order placed succesfully for books \n {items_string}")

        return "payment done"

    def releaseBooks(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        books: list[Books] = db.query(Books).filter(
            Books.user_id == user.id).all()

        items_string = ""
        for i in range(len(books)):

            items_string += f"\n * {books[i].title}"

            books[i].userRented = None
            books[i].bookDetail[0].availability = True

            books[i].bookDetail[0].rented_day = None
            books[i].bookDetail[0].release_day = None

            db.add(books[i])
            db.commit()

            cartitems: list[CartItems] = db.query(CartItems).filter(
                CartItems.book_id == books[i].id).all()

        cartAlertList = {}
        for item in cartitems:
            if item.user.email not in cartAlertList:
                cartAlertList[item.user.email] = []

            cartAlertList[item.user.email].append(item.books.title)

        for email, booknameList in cartAlertList.items():
            items_string = ""
            for book in booknameList:
                items_string += f" \n {book}"
            send_email(
                email, f" Released books \n {items_string}")

        send_email(
            user.email, f" Released books \n {items_string}")

        return
