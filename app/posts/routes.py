from flask import Blueprint, make_response, jsonify, request
from app.posts.model import PostModel
from app.users.model import UserModel
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


post_v1 = Blueprint("post_v1", __name__, url_prefix='/api/v1')

@post_v1.route('/post', methods=['POST'])
@jwt_required()
def post():
    data = request.get_json()
    user_id = get_jwt_identity()
    postpic = data['postpic']
    likes = data['likes']
    body = data['body']
    new_post = PostModel(id=None, user_id=user_id, postpic=postpic, likes=likes, body=body, date_created=datetime.datetime.now())
    new_post.save(user_id=user_id, postpic=postpic, likes=likes, body=body,date_created=datetime.datetime.now() )

    return make_response(jsonify({
        "status": 201,
        "data": new_post.json_dumps(),
        "msg": "posted succesfully"
    }), 201)

@post_v1.route('/post', methods=['GET'])
def get_all_post():
    posts = PostModel.get_all()

    return make_response(jsonify({
        "status":200,
        "data": posts
    }), 200)

@post_v1.route('/post/<int:id>', methods=['GET'])
def get_on(id):

    post = PostModel.get_by_id(id=id)

    if post:
        return make_response(jsonify({
            "status": 200,
            "data": post
        }), 200)
    return make_response(jsonify({
        "status": 404,
        "data": "No Post Found By That ID"
    }), 404)

@post_v1.route('/mypost', methods=['GET'])
@jwt_required()
def get_mypost():

    user = get_jwt_identity()

    posts = PostModel.get_all_user_post(user)

    return make_response(jsonify({
        "status":200,
        "data": posts
    }), 200)

@post_v1.route('/post20', methods=['GET'])
def get_20_post():
    posts = PostModel.get_20_post()

    return make_response(jsonify({
        "status":200,
        "data": posts
    }), 200)

