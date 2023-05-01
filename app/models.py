from app.database.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password: Column(String, nullable=False)
    name = Column(String, nullable=False)
    phoneNumber = Column(Integer, nullable=False)
