from fastapi import status, Depends, APIRouter
from app.database.database import get_db
from app.service.BookDetailService import *
from app.schema.BookDetailSchema import *

router = APIRouter(
    prefix="/bookDetails",
    tags=['Book Details']
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_details_for_a_book(request: BookDetailInput, db:  Session = Depends(get_db)):
    return BookDetailService.addBookDetails(request, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def get_details_for_a_book(book_id: int, db:  Session = Depends(get_db)):
    return BookDetailService.getBookDetails(book_id, db)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_an_existing_details(Book_id: int, db:  Session = Depends(get_db)):
    return BookDetailService.deleteBookDetail(Book_id, db)
