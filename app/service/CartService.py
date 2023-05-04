from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import CartItems
from app.schema.CartSchema import *


class CartService:

    def addItemCart(request: CartInputs, db: Session):
        cartFetch = db.query(CartItems).filter(
            request.user_id == CartItems.user_id).all()

        for i in range(len(cartFetch)):
            if cartFetch[i].book_id in request.book_id:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"item already exists in cart")

        new_cart = []
        for i in range(len(request.book_id)):
            new_cart.append(CartItems(
                rental_period=request.rental_period[i],
                user_id=request.user_id,
                book_id=request.book_id[i]
            ))

        db.add_all(new_cart)
        db.commit()
        db.refresh(new_cart)

        cartFetch = db.query(CartItems).filter(
            request.user_id == CartItems.user_id).all()
        return cartFetch
