import pika
import sys
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_http_response import success

def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)

send()