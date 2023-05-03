from fastapi import status, Depends, APIRouter
from app.service.AuthorService import *
from app.schemas import *
from app.service.BookService import *

router = APIRouter(
    prefix="/book",
    tags=['Book']
)


@router.post("/addBook", status_code=status.HTTP_201_CREATED, response_model=BookOut)
async def to_add_a_book_with_all_the_information(book: Book, db:  Session = Depends(get_db)):
    return BookService.addBook(book, db)


@router.get("", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def to_get_info_of_a_particular_book(bookName: str, db:  Session = Depends(get_db)):
    return BookService.getBooks(bookName, db)


@router.put("/updateUser", status_code=status.HTTP_202_ACCEPTED, response_model=BookResponse)
async def to_update_user_for_a_book(req: updateBookUser, db: Session = Depends(get_db)):
    return BookService.updateBookUser(req, db)
