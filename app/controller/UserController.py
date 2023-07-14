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
    return UserService.signup(user, db)


@router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_user(db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = UserService.getUser(email, db)
    return user


# @router.post("/publish")
def publish_to_rabbitmq(message: str):
    connection = main.get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='fast_api_queue_user')
    try:
        channel.basic_publish(
            exchange='', routing_key='fast_api_queue_user', body=message)
        connection.close()
        return 200
    except Exception as e:
        print(e)

# queue = channel.queue_declare('order_notifys')
# queue_name = queue.method.queue


def get_from_rabbitmq():
    connection = main.get_rabbitmq_connection()
    channel = connection.channel()
    queue = channel.queue_declare(queue='fast_api_queue_user')

    queue_name = queue.method.queue

    channel.queue_bind(
        exchange='order',
        queue=queue_name,
        routing_key='fast_api_queue_user'
    )
    recieved_msg = []

    def callback(ch, method, properties, body):
        payload = json.loads(body)
        recieved_msg.append(payload)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        channel.stop_consuming()

    channel.basic_consume(
        on_message_callback=callback, queue=queue_name)
    channel.start_consuming()
    if len(recieved_msg) > 0:
        return 200, recieved_msg
    else:
        return 404, recieved_msg
