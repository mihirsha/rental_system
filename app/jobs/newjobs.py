from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import printhello
from fastapi import APIRouter
from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import psycopg2

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from app.database.database import get_db
from app.models import BookDetails
from app.utils import send_email
from datetime import datetime, timedelta
app = FastAPI()
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', seconds=3)
def fetch_data():

    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    bookDetails: list[BookDetails] = db.query(BookDetails).filter(
        BookDetails.availability == False).all()
    print(bookDetails)
    for book in bookDetails:
        dt1 = datetime.datetime(book.release_day)
        dt2 = datetime.datetime(datetime.utcnow())
        tdelta = dt2 - dt1
        print(tdelta)
    # Do something with the data, like save it to a file or send it to another API


@app.on_event('shutdown')
async def shutdown_event():
    scheduler.shutdown()
