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
    @classmethod
    def get_followed_users(cls, follower_id):
        format_str = f"""
            SELECT followee_id FROM public.follow WHERE follower_id = '{follower_id}'
        """
        cursor.execute(format_str)
        rows = cursor.fetchall()
        followed_users = []
        for row in rows:
            # If you want just IDs:
            followed_users.append(row[0])
            # If you want to return FollowModel instances:
            # followed_users.append(cls(id=None, follower_id=follower_id, followee_id=row[0]))
        return followed_users
    
    def json_dumps(self):
        '''method to return a json object from the post details'''
        obj = {
            "id": self.id,
            "follower_id": self.follower_id,
            "followee_id": self.followee_id
        }
        return obj

