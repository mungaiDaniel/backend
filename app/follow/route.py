from flask import Blueprint, make_response, jsonify, request
from app.follow.model import FollowModel
from app.users.model import UserModel
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

follow_v1 = Blueprint("follow_v1", __name__, url_prefix='/api/v1')

@follow_v1.route('/follow/<int:id>', methods=['POST'])
@jwt_required()
def follow_user(id):


    follower_id = get_jwt_identity()

    current_user = UserModel.get_id(id)
    if not current_user:
        return jsonify({'message': 'User not found!'}), 404

    followee_id = current_user # Use the user's ID
    if followee_id == follower_id:
        return jsonify({'message': 'You cannot follow yourself!'}), 400

    following = FollowModel(id=None, follower_id=follower_id, followee_id=followee_id)
    following.save(follower_id=follower_id, followee_id=followee_id)

    return make_response(jsonify({
        "status": 201,
        "data": following.json_dumps(),
        "msg": "posted succesfully"
    }), 201)

@follow_v1.route('/unfollow/<int:id>', methods=['POST'])
@jwt_required()
def unfollow_user(id):
    follower_id = get_jwt_identity()

    current_user = UserModel.get_id(id)
    if not current_user:
        return jsonify({'message': 'User not found!'}), 404

    followee_id = current_user # Use the user's ID
    if followee_id == follower_id:
        return jsonify({'message': 'You cannot follow yourself!'}), 400
    
    unfollowing = FollowModel(id=None, follower_id=follower_id, followee_id=followee_id)

    unfollowing.unfollow(follower_id=follower_id, followee_id=followee_id)
    
    return jsonify({"message": "User unfollowed successfully!"})




@follow_v1.route('/following', methods=['GET'])
@jwt_required()
def get_followed_users():
    follower_id = get_jwt_identity()
    followed_users = FollowModel.get_followed_users(follower_id)
    # If you want to return user details, fetch them here
    users_data = []
    for user in followed_users:
        if hasattr(user, 'json_dumps'):
            users_data.append(user.json_dumps())
        elif hasattr(user, 'to_dict'):
            users_data.append(user.to_dict())
        else:
            users_data.append(user)  # fallback: just the ID

    return jsonify({
        "status": 200,
        "data": users_data,
        "msg": "Fetched followed users successfully"
    }), 200



