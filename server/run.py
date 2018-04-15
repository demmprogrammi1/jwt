from models import db,app,User,Post
import json,jwt,datetime
from flask import request,make_response
from flask_jwt import jwt_required
db.create_all()

@app.route('/')
def index():
    return 'Саламалейкум'


@app.route('/register', methods=['POST'])
def add_user():
    bod = request.get_json()
    user = User.query.filter_by(userName=bod['username']).first()
    if user is None:    
        try:
            user = User(userName=bod['username'],
                        password_hash=bod['password'])
            db.session.add(user)
            db.session.commit()
           # token = user.encode_auth_token(user.userId)
           # print(token.__repr__())
            return make_response(json.dumps({
                'message' : 'Successfuly registered',
               # 'auth_token' : token.__repr__()
                }),200)

        except Exception as e:
            return make_response(json.dumps({
                'message' : 'Some problem'
                }),401)                
    else:
        return make_response(json.dumps({
            'message' : 'user with such name already exists'
        }),409)


@app.route('/login', methods=['POST'])
def login():
    bod = request.get_json()
    user = User.query.filter_by(userName=bod['username']).first()
    if user is not None:
        if user.verify_password(bod['password']):
            token = user.encode_auth_token(user.userId)
            return make_response(json.dumps({
                'message' : 'Successfully logined',
                'auth_token' : token.__repr__()
            }),200)
        else:
            return make_response(json.dumps({
                'message' : 'Username and password do not match'
            }),400)
    else:
        return make_response(json.dumps({
            'message' : 'there is no such user'
        }),400)



@app.route('/users/',methods=['GET'])
def get():
    # get the auth token
    auth_token = request.headers.get('Authorization')
    if auth_token is None:
        return make_response(json.dumps({
            'message' : 'no auth header'
        }),400)
    print(auth_token)
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        print(resp)
        user = User.query.filter_by(userId=resp).first()
        print(user)
        posts = Post.query.filter_by(owner=user.userId).all()
        print(posts)
        responseObject = {
            'userData' : user.repr(),
            'userPosts' : posts
        }
        return make_response(json.dumps(responseObject)), 200
    else:
        responseObject = {
            'message': 'Provide a valid auth token.'
        }
        return make_response(json.dumps(responseObject)), 401

@app.route('/add',methods=["POST"])
#@jwt_required()
def create():
    auth = request.headers.get('Authorization')
    if auth is None:
        return make_response(json.dumps({
            'message' : 'no auth token'
        }),401)
    else:
        userId = User.decode_auth_token(auth)
        newPost = request.get_json()
        post = Post(owner=userId,created_at=datetime.datetime.now(),text=newPost['text'])
        db.session.add(post)
        db.session.commit()
        return make_response(json.dumps({
            'message' : 'new post is added'
        }),200)

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
