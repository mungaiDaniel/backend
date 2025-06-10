import json
import unittest
import datetime

from main import app
from database.database import MY_DATABASE
from app.users.model import UserModel
from config import TestingConfig
from helper_function import register_user

class TestUsers(unittest.TestCase):

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
        self.new_user = UserModel(
            id=1,
            name = "name22", 
            username = "username222", 
            email = "email22@com", 
            suite = "suite344", 
            street = "address""street433",
            city = "address""city333",
            zipcode = "address""zipcode333",
            lat = "address""geo""lat333", 
            lng = "address""geo""lng333",
            phone = "phone333", 
            website= "website3333",
            company_name = "company""name3333",
            catchPhrase = "company""catchPhrase3333",
            bs = "company""bs333",
            user_role = "user",
        )
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_init(self):
        self.new_user = UserModel(
            id=1,
            name = "name22", 
            username = "username222", 
            email = "email22@com", 
            suite = "suite344", 
            street = "address""street433",
            city = "address""city333",
            zipcode = "address""zipcode333",
            lat = "address""geo""lat333", 
            lng = "address""geo""lng333",
            phone = "phone333", 
            website= "website3333",
            company_name = "company""name3333",
            catchPhrase = "company""catchPhrase3333",
            bs = "company""bs333",
            user_role = "user",
        )
        self.assertTrue(type(self.new_user.id), int)
        self.assertEqual(type(self.new_user), UserModel)

    
    def test_register(self):
        new_user = {
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "company_name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }
        response = self.client.post('api/v1/register',
                                    data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_all_user(self):
        response = self.client.get('api/v1/user', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_one_user(self):
        data = {
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "company": {
      "company_name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }
        self.client.post( 'api/v1/register', data=json.dumps(data), content_type='application/json' )
        response = self.client.get('api/v1/user/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    

    def test_login(self):
        register_user(self)
        response = self.client.post(
        'api/v1/login',
        data=json.dumps(dict(
            username = "Bret",
            zipcode = "92998-3874"
        )),
        content_type='application/json'
    )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200) 
        self.assertTrue('token' in data)
