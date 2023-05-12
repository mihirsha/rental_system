from passlib.context import CryptContext
from app.constants import regexMobile
from re import fullmatch
import smtplib
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def validMobileNumber(number: str):
    if fullmatch(regexMobile, number) is None:
        return False
    else:
        return True


def send_email(email: str, message: str):

    connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # connection = smtplib.SMTP("smtp.gmail.com", 587)
    # connection.starttls()

    connection.login(user=settings.smtp_mail, password=settings.smtp_password)

    connection.sendmail(from_addr=settings.smtp_mail,
                        to_addrs=email, msg=message)

    connection.quit()
