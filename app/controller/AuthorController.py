from fastapi import status, Depends, APIRouter
from app.service.AuthorService import *
from app.schemas import *

router = APIRouter(
    prefix="/author",
    tags=['Author']
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def signup(author: str, db:  Session = Depends(get_db)):
    return AuthorService.addAuthor(author, db)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_an_existing_author(author: str, db:  Session = Depends(get_db)):
    return AuthorService.deleteAuthor(author, db)
