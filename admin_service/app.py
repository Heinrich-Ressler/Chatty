import pika
import json

def send_admin_action_event(admin_id, action):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    channel.queue_declare(queue='events')

    event = {
        "event": "Admin Action",
        "admin_id": admin_id,
        "action": action
    }

    channel.basic_publish(
        exchange='',
        routing_key='events',
        body=json.dumps(event)
    )

    connection.close()

# Пример использования
send_admin_action_event(42, "Deleted Post 123")
