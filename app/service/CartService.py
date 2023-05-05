from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import CartItems, User
from app.schema.CartSchema import *


class CartService:

    def addItemCart(request: CartInputs, db: Session):

        cartFetch = db.query(CartItems).filter(
            request.user_id == CartItems.user_id).all()

        if len(request.book_id) != len(request.rental_period):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Content list mismatched")

        for i in range(len(cartFetch)):
            if cartFetch[i].book_id in request.book_id:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"item already exists in cart")

        new_cart = []
        for i in range(len(request.book_id)):
            item = CartItems(
                rental_period=request.rental_period[i],
                user_id=request.user_id,
                book_id=request.book_id[i]
            )
            new_cart.append(item)
        db.add_all(new_cart)
        db.commit()
        cartFetch = db.query(CartItems).filter(
            request.user_id == CartItems.user_id).all()
        return cartFetch

    def getCart(user_id: int, db: Session):

        user = db.query(User).filter(user_id == User.id).first()
        if user == None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"user does not exist")

        return user
