from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database.database import get_db
from app.models import Authors, Books
from app.utils import hash, validMobileNumber
from app.schemas import Book, BookOut


class AuthorService:

    def addAuthor(author: str, db: Session):
        authorFetch = db.query(Authors).filter(
            author.strip() == Authors.name).first()
        if authorFetch is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"author already exists")
        else:
            newAuthor = Authors(
                name=author
            )
            db.add(newAuthor)
            db.commit()
            db.refresh(newAuthor)
        return newAuthor

    def deleteAuthor(author: str, db: Session):
        authorFetch = db.query(Authors).filter(
            author.strip() == Authors.name).first()
        if authorFetch is None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"author does not exists")
        else:
            db.delete(authorFetch)
            db.commit()
        return f"deleted author*{author}*"
