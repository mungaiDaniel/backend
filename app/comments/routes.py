from flask import Blueprint, make_response, jsonify, request
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.posts.model import PostModel
from app.users.model import UserModel
from app.comments.model import CommentsModel

comment_v1 = Blueprint('comment_v1', __name__, url_prefix='/api/v1')

@comment_v1.route('comment/<int:id>', methods=['POST'])
@jwt_required()
def post(id):
    post = PostModel.get_by_id(id=id)

    if post == None:
        return make_response(jsonify({
            "status": 404,
            "msg": "No question found"
        }), 404)
    data = request.get_json()
    body = data['body']
    
    user_id = get_jwt_identity()
    email = UserModel.find_email(user_id)

    new_comment = CommentsModel(id=None, body=body, post_id=id, user_id=user_id, email=email, date_created=datetime.datetime.now())

    new_comment.save(body, id, user_id, email, datetime.datetime.now())
    

    return make_response(jsonify({
        "status": 201,
        "msg": "comment posted successfully",
        "data": new_comment.json_dumps()
    }), 201)

@comment_v1.route('/comments/<int:id>', methods=['GET'])
def get_all(id):
    all_comments = CommentsModel.get_all_post_comments(post_id=id)

    return make_response(jsonify({
        "status": 200,
        "data": all_comments
    }), 200)

@comment_v1.route('/comment/<int:id>', methods=['GET'])
def get_by_id(id):
    comment = CommentsModel.get_by_id(id=id)
    if comment:
        return make_response(jsonify({
            "status": 200,
            "data": comment
        }), 200)
    return make_response(jsonify({
        "status": 404,
        "data": "No comment found by that id"
    }), 404)
