from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from app.models import BookDetails, User
from app.utils import send_email
from datetime import datetime, timedelta

app = FastAPI()
scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=720)
def fetch_data():

    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    bookDetails: list[BookDetails] = db.query(BookDetails).filter(
        BookDetails.availability == False).all()
    users = {}
    overdue = {}
    for book in bookDetails:
        # date = book.release_day.date()
        # deltatime = datetime.strptime(f"{date}", "%Y-%m-%d")
        # print(deltatime.day)

        date = book.release_day.date()-datetime.utcnow().date()
        # date = book.release_day-datetime.utcnow()

        # print(date)

        # dt1 = datetime.day(book.release_day)
        # dt2 = datetime(datetime.utcnow())
        # tdelta = dt2 - dt1
        # print(tdelta, " ", book.book_id)

        if date.days <= 1 and 0 < date.days:
            user: User = db.query(User).filter(
                User.id == book.book.user_id).first()

            users[user.email] = book.book.title
            print(user.email)

        if date.days <= 1 and 0 > date.days:
            user: User = db.query(User).filter(
                User.id == book.book.user_id).first()

            overdue[user.email] = book.book.title

    for mailid, bookname in users.items():
        send_email(mailid, f"{bookname} is about to expire")

    for mailid, bookname in overdue.items():
        send_email(mailid, f"{bookname} is already expired")

    print("mail sent successfully")

    print("------------")
    # Do something with the data, like save it to a file or send it to another API


@app.on_event('shutdown')
async def shutdown_event():
    scheduler.shutdown()
