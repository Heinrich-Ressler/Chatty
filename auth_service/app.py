import pika
import json

def send_user_registered_event(user_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='events')

    event = {"event": "User Registered", "user_id": user_id}
    channel.basic_publish(exchange='', routing_key='events', body=json.dumps(event))

    connection.close()

# Пример использования
send_user_registered_event(123)
