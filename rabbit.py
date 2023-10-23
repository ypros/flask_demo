import pika
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
import json

url = "amqp://guest:guest@localhost/"
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)
channel = connection.channel()

exchange = "flask-exchange"
routing_key = "post-create"
queue = "flask-queue"
channel.exchange_declare(exchange, durable=True)

def add_post_friends(user_id, post_id, friends, text):
    payload = json.dumps({
        'user_id': user_id,
        'post_id': post_id,
        'text': text,
        'friends': list(friends)
    })

    channel.basic_publish(exchange, routing_key, str(payload).encode("utf-8"), mandatory=True)

def add_post(user_id, text):
    payload = json.dumps({
        'user_id': user_id,
        'text': text,
    })

    channel.basic_publish(exchange, routing_key, str(payload).encode("utf-8"), mandatory=True)
