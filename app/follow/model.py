from datetime import datetime
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from database.database import MY_DATABASE

cursor = MY_DATABASE.connect_to_db()

class FollowModel(MY_DATABASE):

    def __init__(self, id, follower_id, followee_id):
        self.id = id
        self.follower_id = follower_id
        self.followee_id = followee_id

    def save(self, follower_id, followee_id):
        format_str = f"""
                  INSERT INTO public.follow (follower_id, followee_id)
                 VALUES ('{follower_id}', '{followee_id}')
 """
        cursor.execute(format_str)
        return{
            "follower_id": follower_id,
            "followee_id": followee_id
        }
    @classmethod
    def unfollow(cls, follower_id, followee_id):
        format_str = f"""
                  DELETE FROM public.follow WHERE follower_id = '{follower_id}' AND followee_id = '{followee_id}'
 """
        cursor.execute(format_str)

        return{
            "message" : "unfollow successfully"
        }

    
    def json_dumps(self):
        '''method to return a json object from the post details'''
        obj = {
            "id": self.id,
            "follower_id": self.follower_id,
            "followee_id": self.followee_id
        }
        return obj

