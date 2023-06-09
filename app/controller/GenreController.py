from fastapi import status, Depends, APIRouter
from app.database.database import get_db
from app.service.GenreService import *
from app.schema.GenreSchema import *

router = APIRouter(
    prefix="/genre",
    tags=['Genre']
)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_a_new_genre(genre: str, db:  Session = Depends(get_db)):
    return GenreService.addGenre(genre, db)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_an_existing_genre(genre: str, db:  Session = Depends(get_db)):
    return GenreService.deleteGenre(genre, db)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=GenresResponse)
async def fetch_an_existing_genre(genre: str, db:  Session = Depends(get_db)):
    return GenreService.getGenre(genre, db)
