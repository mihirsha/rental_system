from fastapi import status, Depends, APIRouter
from app.schema.UserSchema import Signup
from sqlalchemy.orm import Session
from app.service.UserService import *
from app.database.database import get_db
from app.schema.UserSchema import UserOut
from app.oauth2 import get_current_user
from app import main as main


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def signup(user: Signup, db:  Session = Depends(get_db)):
    status, msg = UserService.signup(user, db)
    if status == 406:
        raise HTTPException(status_code=406)
    return msg


@router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_user(db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = UserService.getUser(email, db)
    return user


# def check_queue_exists(queue_name):
#     # Establish a connection to RabbitMQ
#     connection = main.get_rabbitmq_connection()
#     channel = connection.channel()

#     # Declare the queue
#     try:
#         queue_declare_result = channel.queue_declare(
#             queue=queue_name, passive=True)
#         exists = True
#     except pika.exceptions.ChannelClosedByBroker:
#         exists = False

    # Close the connection
    # connection.close()

    # return exists


# ----------------------------------------------

# def upgrade() -> None:
#     op.alter_column('user', 'id', sa.Column(
#         UUID, primary_key=True, nullable=False))
#     pass


# def downgrade() -> None:
#     op.alter_column('user', 'id', sa.Column(
#         Integer, primary_key=True, nullable=False, autoincrement=True))
#     pass
