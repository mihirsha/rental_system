from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from app.models import BookDetails
from app.utils import send_email
from datetime import datetime, timedelta
import sys
import time
import asyncio


def printhello(db: Session):

    print(db)
    bookDetails: list[BookDetails] = db.query(BookDetails).filter(
        BookDetails.availability == False).all()

    for book in bookDetails:

        dt1 = datetime.datetime(book.release_day)
        dt2 = datetime.datetime(datetime.utcnow())
        tdelta = dt2 - dt1
        print(tdelta)

    # helper()

    # send_email("mihir.shah@sleevesup.com.au", f"{datetime.utcnow()}")
    # print("mail sent")
