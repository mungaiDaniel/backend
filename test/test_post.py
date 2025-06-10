import json
import unittest

from main import app
from database.database import MY_DATABASE
from app.posts.model import PostModel
from config import TestingConfig
from helper_function import register_user
from helper_function import post_posts ,register_user, login_user

class TestPost(unittest.TestCase):

    def tearDown(self):
        MY_DATABASE.drop_users_table()
        MY_DATABASE.drop_post_table()
        MY_DATABASE.drop_comment_table()
        MY_DATABASE.create_user_table()
        MY_DATABASE.create_post_table()
        MY_DATABASE.create_comments_table()

    def setUp(self):
        # setting up configurations for testing
        self.app = app
        self.app.config.from_object(TestingConfig)
        self.new_post = PostModel(id=4, title="how to init python",
                                     body="how to init python how to init python how to init python", user_id=1)
        self.client = self.app.test_client()
        self.app.testing = True
        register_user(self)
        response = login_user(self)
        self.token = json.loads(response.data.decode())['token']

    def test_posts(self):
        response = post_posts(self)
        self.assertEqual(response.status_code, 201)

    def test_get_a_single_post(self):
        # test can get a single post
        post_posts(self)
        response = self.client.get(f'api/v1/post/1', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_post(self):
        # test can get a none existing post
        response = self.client.get(f'api/v1/post/145678', content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_get_all_post(self):
        # test can get all post
        response = self.client.get('/api/v1/post', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(response), list)