import json
from pika import BlockingConnection, ConnectionParameters


def get_rabbitmq_connection():
    return BlockingConnection(ConnectionParameters('rabbitmq'))


def publish_to_rabbitmq(message: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queue_declare_result = channel.queue_declare(queue='fast_api_queue_user')
    # queue_length = queue_declare_result.method.message_count

    try:
        channel.basic_publish(
            exchange='', routing_key='fast_api_queue_user', body=message)
        connection.close()
        return 200
    except Exception as e:
        print(e)


def get_from_rabbitmq():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    queue_declare_result = channel.queue_declare(
        queue='fast_api_queue_user')

    queue_name = queue_declare_result.method.queue
    queue_length = queue_declare_result.method.message_count

    count = queue_length

    recieved_msg = []

    def callback(ch, method, properties, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        nonlocal count
        count -= 1
        if count >= 0:
            payload = json.loads(body)
            recieved_msg.append(payload)
        else:
            channel.stop_consuming()

    channel.basic_consume(
        on_message_callback=callback, queue=queue_name)
    if queue_length > 0:
        channel.start_consuming()
    return recieved_msg
