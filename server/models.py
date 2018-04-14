from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt,json
import datetime
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'Users'

    userId = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    userName = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    '''
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    '''
    def verify_password(self, password):
        return password == self.password_hash

    def repr(self):
        return {
            'User': self.userName,
        }

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print("exception in encode in models")
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Post(db.Model):
    __tablename__ = 'Posts'

    post_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('Users.userId'),nullable=False, unique=False,primary_key=True)
    created_at = db.Column(db.DateTime)
    text = db.Column(db.Text)

    def repr(self):
        return {
            'post_id' : self.post_id,
            'owner' : self.owner,
            'created_at' : self.created_at,
            'text' : self.text
        }