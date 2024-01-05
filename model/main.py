from transformers import pipeline
pipe = pipeline("text-classification", model="ProsusAI/finbert")

import pika
import time
import numpy as np
# load numpy array
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def handle(msg):
    res = pipe(msg)
    return res

# rabbitmq 
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):
    msg = body.decode()
    logging.info('On request: '+msg)
    ch.basic_publish(
        exchange='',
        routing_key=str(props.reply_to),
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(handle(msg))
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

print("Awaiting RPC requests...")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
channel.start_consuming()