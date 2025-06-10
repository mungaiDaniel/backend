from datetime import datetime
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from app.users.model import UserModel
from app.comments.model import CommentsModel
from database.database import MY_DATABASE
        
cursor = MY_DATABASE.connect_to_db()
MY_DATABASE.create_user_table()
MY_DATABASE.create_post_table()
        
class PostModel(MY_DATABASE):
    '''Class to model a post'''

    def __init__(self,id, user_id, postpic, likes, body, date_created):
        '''method to initialize postModal class'''
        self.id = id
        self.user_id = user_id
        self.postpic = postpic
        self.likes = likes
        self.body = body
        self.date_created = date_created

    def save(self , user_id , postpic, likes,  body, date_created):
        '''method to save a post'''
        format_str = f"""
         INSERT INTO public.post (user_id,postpic,likes,body,date_created)
         VALUES ('{user_id}', '{postpic}','{likes}','{body}', '{str(datetime.datetime.now())}') ;
         """
        cursor.execute(format_str)
        return {
            "user_id": user_id,
            "postpic": postpic,
            "likes": likes,
            "body": body,
            "date_created": str(date_created)
            
        }
    def json_dumps(self):
        '''method to return a json object from the post details'''
        obj = {
            "id": self.id,
            "user_id": self.user_id,
            "postpic": self.postpic,
            "likes": self.likes,
            "body": self.body,
            "date_created": str(self.date_created),
            "comments": CommentsModel.get_all_post_comments(self.id)
        }
        return obj
    
    @classmethod
    def get_by_id(cls, id):
        '''method to get a post by id'''
        cursor.execute('SELECT * FROM "public"."post" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row == None:
            return None
        posts = PostModel(id=row[0], user_id=row[1], postpic=row[2], likes=row[3], body=row[4], date_created=row[5])

        retrieved_post = posts.json_dumps()
        comment = CommentsModel.get_all_post_comments(post_id=id)
        retrieved_post['comments'] = comment
        return retrieved_post
    @classmethod
    def get_all(cls):
        '''method to get all posts'''
        cursor.execute(
            f"SELECT * FROM public.post")
        rows = cursor.fetchall()
        list_dict = []

        for item in rows:
            new = PostModel(id=item[0], user_id=item[1], postpic=item[2], likes=item[3], body=item[4], date_created=item[5])
            list_dict.append(new.json_dumps())
        return list_dict

    @classmethod
    def get_all_user_post(cls, user):
        '''method to get all posts of a given user'''
        post_owner = UserModel.find_by_id(user)
        if post_owner:
            cursor.execute("SELECT * FROM public.post WHERE user_id = %s", (user,))
            rows = cursor.fetchall()
            list_dict = []

            for item in rows:
                new = PostModel(id=item[0], user_id=item[1], postpic=item[2], likes=item[3], body=item[4], date_created=item[5])
                list_dict.append(new.json_dumps())
            return list_dict
        return {"message": "No user with that id"}, 404

    @classmethod
    def delete_post(cls, id):
        '''method to delete a post'''
        try:
            cursor.execute('DELETE FROM public.post CASCADE WHERE id = %s', (id,))
            return "successfully deleted"
        except Exception:
            return "failed"

    @classmethod
    def search_post(cls, body, title):
        cursor.execute(f"SELECT * FROM post WHERE body LIKE '%{body}%'")
        rows = cursor.fetchall()
        list_dict = []
        for item in rows:
            new = PostModel(id=item[0], user_id=item[1], postpic=item[2], likes=item[3], body=item[4], date_created=item[5])
            list_dict.append(new.json_dumps())
        return list_dict
    
    @classmethod
    def get_20_post(cls):
        '''method to get all posts'''
        cursor.execute(
            f"SELECT * FROM public.post LIMIT 20")
        rows = cursor.fetchall()
        list_dict = []

        for item in rows:
            new = PostModel(id=item[0], user_id=item[1], postpic=item[2], likes=item[3], body=item[4], date_created=item[5])
            list_dict.append(new.json_dumps())
        return list_dict

