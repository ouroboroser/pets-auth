from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_http_response import success
import pika
import sys
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456789@localhost:5432/pets"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
"db.create_all()"

from service import AuthService
service = AuthService()

@app.route('/')
def hello_world():
    return 'authorization service'

@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        users = service.getusers()
        result = json.dumps(users, default=str)
        return result
    if request.method == 'POST':
        user = request.get_json()
        return service.signup(user)
    if request.method == 'PUT':
        return service.update()
    if request.method == 'DELETE':
        return service.delete()

@app.route('/auth-path-1')
def auth_path_1():
    return success.return_response(message='successfully completed request to auth path 1', status=200)

@app.route('/auth-path-2')
def auth_path_2():
    return success.return_response(message='successfully completed request to auth path 2', status=200)

@app.route('/auth-path-3', methods=['GET'])
def auth_path_3():
    url = "http://34.121.67.167/pets-service/service-path-3"

    payload = {}
    headers = {
        'Host': 'app.pets'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

@app.route('/send', methods=['POST'])
def send():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='pets:pets@my-release-rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)
    connection.close()
    return {message: "success"}

@app.route('/receive', methods=['GET'])
def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='pets:pets@my-release-rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    queue_name = "my queue"
    channel.queue_declare(queue=queue_name, exclusive=True)

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    return {"status": "success"}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
