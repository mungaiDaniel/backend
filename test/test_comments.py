import json
import unittest
import datetime

from main import app
from database.database import MY_DATABASE
from config import TestingConfig
from helper_function import register_user
from helper_function import post_posts, register_user, login_user, post_comments

class TestComment(unittest.TestCase):

    def tearDown(self):
        MY_DATABASE.drop_users_table()
        MY_DATABASE.drop_post_table()
        MY_DATABASE.drop_comment_table()
        MY_DATABASE.create_user_table()
        MY_DATABASE.create_post_table()
        MY_DATABASE.create_comments_table()

    def setUp(self):
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        register_user(self)
        post_posts(self)
        self.client = self.app.test_client()
        self.app.testing = True

    def test_answer_posted(self):
        '''test that an comment can be posted'''
        response = login_user(self)
        result = json.loads(response.data)
        self.assertIn("token", result)
        new_comment = {"name":" kndwjwdjsnksia ",  'body': 'errossssssssssssssssssssssssssssssssssssssssssssssssss'}
        response = self.client.post('/api/v1/comment/1', data=json.dumps(new_comment),
                                    headers={'Authorization': f'Bearer {result["token"]}',
                                             'Content-Type': 'application' '/json'})
        self.assertEqual(response.status_code, 201)

    def test_get_all_comment(self):
        # test can get all comment
        response = self.client.get('/api/v1/comments/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response), list)

    def test_get_a_single_comment(self):
        # test can get a single commeny
        post_comments(self)
        response = self.client.get(f'api/v1/comment/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
