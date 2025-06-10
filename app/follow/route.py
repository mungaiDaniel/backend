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

    followee_id = current_user.id  # Use the user's ID
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

    followee_id = current_user.id  # Use the user's ID
    if followee_id == follower_id:
        return jsonify({'message': 'You cannot follow yourself!'}), 400
    
    unfollowing = FollowModel(id=None, follower_id=follower_id, followee_id=followee_id)

    unfollowing.unfollow(follower_id=follower_id, followee_id=followee_id)
    
    return jsonify({"message": "User unfollowed successfully!"})








