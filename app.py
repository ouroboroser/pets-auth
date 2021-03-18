from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_http_response import success, result, error

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

@app.route('/auth-path-3')
def auth_path_3():
    response = requests.get('http://127.0.0.1:3000/service-path-3').content
    print(response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
