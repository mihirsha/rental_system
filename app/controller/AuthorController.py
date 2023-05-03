from fastapi import status, Depends, APIRouter
from app.database.database import get_db
from app.service.AuthorService import *
from app.schema.AuthorSchema import *

router = APIRouter(
    prefix="/author",
    tags=['Author']
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def to_add_a_new_author(author: str, db:  Session = Depends(get_db)):
    return AuthorService.addAuthor(author, db)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_an_existing_author(author: str, db:  Session = Depends(get_db)):
    return AuthorService.deleteAuthor(author, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=AuthorForGet)
async def to_get_an_existing_author(author: str, db:  Session = Depends(get_db)):
    return AuthorService.getAuthor(author, db)
