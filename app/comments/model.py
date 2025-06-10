
import datetime
from database.database import MY_DATABASE


        
cursor = MY_DATABASE.connect_to_db()
MY_DATABASE.create_user_table()
MY_DATABASE.create_post_table()
MY_DATABASE.create_comments_table()
        
class CommentsModel(MY_DATABASE):
    '''Class to model an comment'''

    def __init__(self, id, body, post_id, user_id, email, date_created):
        '''method to initialize commentMedel class'''
        self.id = id
        self.body = body
        self.post_id = post_id
        self.user_id = user_id
        self.email = email
        self.date_created = date_created

    def save(self, body, post_id, user_id, email, date_created):
        '''method to save an comment'''
        format_str = f"""INSERT INTO public.comment (body, post_id, user_id, email, date_created)
                 VALUES ('{body}', '{post_id}', '{user_id}', '{email}', '{str(datetime.datetime.now().date())}');
                 """
        cursor.execute(format_str)
        return {
            "body": body,
            "post_id": post_id,
            "user_id": user_id,
            "email": email,
            "date_created": str(date_created)
        }
        
    def json_dumps(self):
        '''method to return a json object from the comment details'''
        
        obj = {
            "id": self.id,
            "body": self.body,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "email": self.email,
            "date_created": str(self.date_created)
            
        }
        return obj

    @classmethod
    def get_all_post_comments(cls, post_id):
        '''method to get all comments of a given question'''
        cursor.execute(
            f"SELECT * FROM public.comment")
        rows = cursor.fetchall()
        comments_retrieved_dict = []
        for comment in rows:
            if comment[3] == (post_id):
                comment_post = CommentsModel(id=comment[0], body=comment[1], post_id=comment[2],
                                         user_id=comment[3], email=comment[4], date_created=comment[5])
                comments_retrieved_dict.append(comment_post.json_dumps())
        return comments_retrieved_dict

    @classmethod
    def get_by_id(cls, id):
        '''method to get an comment by id'''
        cursor.execute('SELECT * FROM "public"."comment" WHERE id=%s', (id,))
        row = cursor.fetchone()
        if row == None:
            return None
        comment = {
            "id": row[0],
            "body": row[1],
            "post_id": row[2],
            "user_id": row[3],
            "email": row[4],
            "date_created": row[5]
        }
        retrieved_comment = comment
        return retrieved_comment

    @classmethod
    def update(cls, body,  user_id, id):
        """Method to update an comment"""
        format_str = f"""
         UPDATE public.comment SET body = '{body}' WHERE id = {id};
         """

        cursor.execute(format_str)

        return {
            "id": id,
            "body": body,
            "user_id": user_id,
        }