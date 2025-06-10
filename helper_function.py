import json

def register_user(self):
    '''register user'''
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
    return self.client.post(
        'api/v1/register',
        data=json.dumps(new_user),
        content_type='application/json'
    )

def register_user2(self):
    '''register user'''
    return self.client.post(
        'api/v1/register',
        data=json.dumps(dict(
            name = "name22", 
            username = "username222", 
            email = "email22@com", 
            street = "address""street433",
            suite = "address""suite344", 
            city = "address""city333",
            zipcode = "address""zipcode333",
            lat = "address""geo""lat333", 
            lng = "address""geo""lng333",
            phone = "phone333", 
            website= "website3333",
            campany_name = "company""name3333",
            catchPhrase = "company""catchPhrase3333",
            bs = "company""bs333",
            user_role = "user",
        )),
        content_type='application/json'
    )
    
def login_user(self):
    '''login the registered user'''
    return self.client.post(
        'api/v1/login',
        data=json.dumps(dict(
            username = "Bret",
            zipcode = "92998-3874"
        )),
        content_type='application/json'
    )
    
def post_posts(self):
    
    response = login_user(self)
    result = json.loads(response.data)
    self.assertIn("token", result)
    new_post = {'user_id': 1, 'title': 'error sit voluptatem accusantium doloremque laudantium',
                    'body': 'error sit voluptatem accusantium doloremque laudantiumerror sit volupta'}
    response = self.client.post('api/v1/post', data=json.dumps(new_post),
                                headers={'Authorization': f'Bearer {result["token"]}',
                                         'Content-Type': 'application' '/json'})
    return response

def post_comments(self):
    
    response = login_user(self)
    result = json.loads(response.data)
    self.assertIn("token", result)
    new_comment = {"name":" kndwjwdjsnksia ",  'body': 'errossssssssssssssssssssssssssssssssssssssssssssssssss'}
    response = self.client.post('/api/v1/comment/1', data=json.dumps(new_comment),
                                    headers={'Authorization': f'Bearer {result["token"]}',
                                             'Content-Type': 'application' '/json'})
    return response