from fastapi import status, Depends, APIRouter, UploadFile, File, logger, Form
from app.service.AuthorService import *
from app.database.database import get_db
from app.schema.BookSchema import *
from app.service.BookService import *

router = APIRouter(
    prefix="/book",
    tags=['Book']
)


@router.post("/addBook", status_code=status.HTTP_201_CREATED, response_model=BookOut)
async def to_add_a_book_with_all_the_information(book: Book = Depends(), file: UploadFile = File(...), db:  Session = Depends(get_db)):
    return await BookService.addBook(book, db, file)


# response_model=BookResponse_file)
@router.get("", status_code=status.HTTP_200_OK)
async def to_get_info_of_a_particular_book(bookName: str, db:  Session = Depends(get_db)):
    return BookService.getBooks(bookName, db)


@router.get("/download", status_code=status.HTTP_200_OK)
async def to_get_info_of_a_particular_book(bookName: str, db:  Session = Depends(get_db)):
    return BookService.downloadBooks(bookName, db)


@router.put("/updateBook", status_code=status.HTTP_202_ACCEPTED, response_model=BookResponse)
async def to_update_user_for_a_book(req: updateBookUser, db: Session = Depends(get_db)):
    return BookService.updateBookUser(req, db)


@router.delete("/deleteBook", status_code=status.HTTP_200_OK)
async def to_delete_a_book(book_id: int, db: Session = Depends(get_db)):
    return BookService.deleteBook(book_id, db)
