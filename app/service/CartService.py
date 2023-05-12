from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import CartItems, User, BookDetails
from app.schema.CartSchema import *


class CartService:

    def addItemCart(email: str, request: CartInputs, db: Session):

        user = db.query(User).filter(
            email == User.email).first()

        cartFetch = db.query(CartItems).filter(
            user.id == CartItems.user_id).all()

        if len(request.book_id) != len(request.rental_period):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Content list mismatched")

        for i in range(len(cartFetch)):
            if cartFetch[i].book_id in request.book_id:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book with id {cartFetch[i].book_id} already exists in cart")

        new_cart = []
        for i in range(len(request.book_id)):

            bookDetail = db.query(BookDetails).filter(
                BookDetails.book_id == request.book_id[i]).first()

            if bookDetail == None:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Details for book_id {request.book_id[i]} is not available")
            elif bookDetail.availability:
                item = CartItems(
                    rental_period=request.rental_period[i],
                    user_id=user.id,
                    book_id=request.book_id[i]
                )
                new_cart.append(item)
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book with id {request.book_id[i]} is not available")

        db.add_all(new_cart)
        db.commit()
        cartFetch = db.query(CartItems).filter(
            user.id == CartItems.user_id).all()
        return cartFetch

    def getCart(email: str, db: Session):

        user = db.query(User).filter(email == User.email).first()
        if user == None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user does not exist")
        return user

    def deleteCart(request: CartDelete, email: str, db: Session):
        user = db.query(User).filter(
            email == User.email).first()

        cartFetch = db.query(CartItems).filter(
            user.id == CartItems.user_id).all()

        deleteList: list[CartItems] = []
        for id in request.book_id:
            for cart in cartFetch:
                if cart.book_id == id:
                    deleteList.append(cart)

        if deleteList == []:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Item requested to delete not found in cart")

        for item in deleteList:
            db.delete(item)
            db.commit()

        return "items deleted"
