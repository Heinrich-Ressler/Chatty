import pika
import json

def send_post_created_event(post_id, user_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='events')

    event = {"event": "Post Created", "post_id": post_id, "user_id": user_id}
    channel.basic_publish(exchange='', routing_key='events', body=json.dumps(event))

    connection.close()

# Пример использования
send_post_created_event(456, 123)
