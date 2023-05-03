from fastapi import status, Depends, APIRouter
from app.service.GenreService import *
from app.schemas import *

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
