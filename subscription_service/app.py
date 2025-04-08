import pika
import json

def callback(ch, method, properties, body):
    event = json.loads(body)
    print(f"Received event: {event}")
    if event['event'] == "User Registered":
        # Логика обработки события "User Registered"
        pass

def listen_for_events():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='events')

    channel.basic_consume(queue='events', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Пример использования
listen_for_events()
