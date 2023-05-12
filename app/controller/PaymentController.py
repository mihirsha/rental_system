from fastapi import status, Depends, APIRouter
from app.database.database import get_db
from app.service.PaymentService import *
from app.schema.PaymentSchema import *
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/payment",
    tags=['Payments']
)


@router.post("/add", status_code=status.HTTP_200_OK)
async def add_payement_for_a_book(db:  Session = Depends(get_db), email: str = Depends(get_current_user)):
    return PaymentService.paymentAdd(email, db)


@router.put("/remove", status_code=status.HTTP_200_OK)
async def release_books_held(db:  Session = Depends(get_db), email: str = Depends(get_current_user)):
    return PaymentService.releaseBooks(email, db)


# @router.delete("/delete", status_code=status.HTTP_200_OK)
# async def delete_an_existing_genre(user_id: int, db:  Session = Depends(get_db)):
#     return BookDetailService.deleteBookDetail(user_id, db)
