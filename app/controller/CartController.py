from fastapi import status, Depends, APIRouter
from app.database.database import get_db
from app.service.CartService import *
from app.schema.CartSchema import *
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=['Cart']
)


@router.post("/addItems", status_code=status.HTTP_201_CREATED)
async def add_items_to_the_cart(request: CartInputs, db:  Session = Depends(get_db), email: str = Depends(get_current_user)):
    return CartService.addItemCart(email, request, db)


@router.get("/getItem", status_code=status.HTTP_200_OK, response_model=UserOut)
async def add_items_to_the_cart(db:  Session = Depends(get_db), email: str = Depends(get_current_user)):
    cart = CartService.getCart(email, db)
    return cart


@router.delete("/deleteItem", status_code=status.HTTP_200_OK)
async def add_items_to_the_cart(request: CartDelete, db:  Session = Depends(get_db), email: str = Depends(get_current_user)):
    cart = CartService.deleteCart(request, email, db)
    return cart
