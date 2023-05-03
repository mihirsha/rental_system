from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database.database import get_db
from app.models import Genre, association_book_genre
from app.utils import hash, validMobileNumber
from app.schemas import GenresResponse


class GenreService:

    def addGenre(genre: str, db: Session):
        genreFetch = db.query(Genre).filter(
            genre.strip() == Genre.name).first()
        if genreFetch is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Genre already exists")
        else:
            newGenre = Genre(
                name=genre
            )
            db.add(newGenre)
            db.commit()
            db.refresh(newGenre)
        return newGenre

    def deleteGenre(genre: str, db: Session):
        genreFetch = db.query(Genre).filter(
            genre.strip() == Genre.name).first()
        if genreFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Genre does not exists")
        else:
            db.delete(genreFetch)
            db.commit()
        return f"deleted genre *{genre}*"

    def getGenre(genre: str, db: Session):
        genreFetch: Genre = db.query(Genre).filter(
            genre.strip() == Genre.name).first()

        if genreFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Genre does not exists")

        print(genreFetch.books)

        return GenresResponse(
            id=genreFetch.id,
            name=genreFetch.name,
            books=genreFetch.books
        )
