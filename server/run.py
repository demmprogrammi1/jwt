from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from models import *

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'Саламалейкум'


@app.route('/register', methods=['POST'])
def add_user():
    json = request.get_json()
    user = User.query.filter_by(userName=json['username']).first()
    if user is None:
        user = User(userName=json['username'],
                    password=json['password'])
    else:
        return 'Username "%s" already exists!' % json['username']
    db.session.add(user)
    db.session.commit()
    return 'Hello %s!' % user.userName


@app.route('/login', methods=['POST'])
def login():
    json = request.get_json()
    user = User.query.filter_by(userName=json['username']).first()
    if user is not None and user.verify_password(json['password']):
        return 'Successful!'
    else:
        return 'Wrong!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
