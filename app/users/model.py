from datetime import datetime
import datetime
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from database.database import MY_DATABASE


cursor = MY_DATABASE.connect_to_db()

class UserModel(MY_DATABASE):
    def __init__(self,id, name, username, email, street, suite,city,zipcode,lat,lng,phone,website,company_name , catchPhrase, bs, user_role, personPic,date_created):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.street = street
        self.suite = suite
        self.city = city
        self.zipcode = zipcode
        self.lat = lat
        self.lng = lng
        self.phone = phone
        self.website = website
        self.company_name = company_name
        self.catchPhrase = catchPhrase
        self.bs = bs
        self.user_role = user_role
        self.personPic = personPic
        self.date_created = date_created

    

    def save(self, name, username, email, street, suite,city,zipcode,lat,lng,phone,website,company_name , catchPhrase, bs, user_role, personPic, date_created):
        format_str = f"""
                 INSERT INTO public.user (name, username, email, street, suite, city, zipcode, lat, lng, phone, website, company_name, catchPhrase, bs, user_role, personPic, date_created)
                 VALUES ('{name}', '{username}', '{email}', '{street}', '{suite}', '{city}', '{zipcode}', '{lat}', '{lng}', '{phone}', '{website}', '{company_name}', '{catchPhrase}', '{bs}', '{user_role}', '{personPic}', '{str(datetime.datetime.now().date())}')

                 """
        cursor.execute(format_str)
        return {
             "name": name, 
            "username": username, 
            "email": email, 
            "street": street,
            "address":{
                "suite": suite, 
            "city": city, 
            "zipcode": zipcode, 
            "lat": lat, 
            "lng": lng,
            } ,
             
            "phone": phone, 
            "website": website,
            "company":{
                 "company_name": company_name, 
            "catchPhrase": catchPhrase, 
            "bs": bs 
            },
            "user_role": user_role, 
            "personPic": personPic,
            "date_created": str(date_created)
        }

    def generate_auth_token(self, permission_level):

    
        if permission_level == 1:

            token = create_access_token(identity=self.id, additional_claims={'admin': 1})

            return token

        return create_access_token(identity=self.id, additional_claims={'admin': 0})

    @staticmethod
    def generate_hash(zipcode):
        '''method that returns a hash'''
        return pbkdf2_sha256.hash(zipcode)

    @staticmethod
    def verify_hash(zipcode, hash):
        '''method to verify zipcode with the hash'''
        return pbkdf2_sha256.verify(zipcode, hash)
    
    def json_dumps(self):
        '''method to return a json object from a user'''
        ans = { 
            "id": self.id,
           "name": self.name, 
            "username": self.username, 
            "email": self.email, 
            "address":{
            "street": self.street,
            "suite": self.suite, 
            "city": self.city, 
            "zipcode": self.zipcode, 
            "lat": self.lat, 
            "lng": self.lng,
            } ,
             
            "phone": self.phone, 
            "website": self.website,
            "company":{
                 "company_name": self.company_name, 
            "catchPhrase": self.catchPhrase, 
            "bs": self.bs 
            },
            "user_role": self.user_role,
            "personPic": self.personPic,
            "date_created": str(self.date_created) 
           
        }
        return ans
    
    @classmethod
    def find_by_email(cls, email):
        '''This method gets a user using email'''
        try:
            format_str = f"""SELECT * FROM \"user\" WHERE email = '{email}' 
                        """
            cursor.execute(format_str)
            user = cursor.fetchone()
            return list(user)
        except Exception as e:
            return {'error': e}

    @classmethod
    def find_by_username(cls, username):
        '''method to find a user by username'''
        try:
            format_str = f"""SELECT * FROM \"user\" WHERE username = '{username}'  LIMIT 1
                        """
            cursor.execute(format_str)
            user = cursor.fetchone()
            return list(user)
        except Exception as e:
            print('::::::', e)
            return {'error': e}

    @classmethod
    def find_by_id(cls, id):
        '''method to find a user by id'''
        try:
            format_str = f"""SELECT * FROM \"user\" WHERE id = id  LIMIT 1
                        """
            cursor.execute(format_str)
            retrieved_user = list(cursor.fetchone())
            user = UserModel(id=retrieved_user[0], name=retrieved_user[1], username=retrieved_user[2], email=retrieved_user[3], street=retrieved_user[4], suite=retrieved_user[5], city=retrieved_user[6], zipcode=retrieved_user[7], lat=retrieved_user[8],lng=retrieved_user[9], phone=retrieved_user[10],website=retrieved_user[11], company_name=retrieved_user[12],catchPhrase=retrieved_user[13], bs=retrieved_user[14], user_role=retrieved_user[15], personPic=retrieved_user[16], date_created=retrieved_user[17])

            return user.json_dumps()
        except Exception as e:
            return {"error": e}
        
    @classmethod
    def find_email(cls, id):
        '''method to find am email'''
        try:
            format_str = f"""SELECT * FROM public.user WHERE id = {id}  LIMIT 1
                        """
            cursor.execute(format_str)
            retrieved_user = list(cursor.fetchone())
            user = UserModel(id=retrieved_user[0], name=retrieved_user[1], username=retrieved_user[2], email=retrieved_user[3], street=retrieved_user[4], suite=retrieved_user[5], city=retrieved_user[6], zipcode=retrieved_user[7], lat=retrieved_user[8],lng=retrieved_user[9], phone=retrieved_user[10],website=retrieved_user[11], company_name=retrieved_user[12],catchPhrase=retrieved_user[13], bs=retrieved_user[14], user_role=retrieved_user[15], personPic=retrieved_user[16], date_created=retrieved_user[17])

            return user.email
        except Exception as e:
            return {"error": e}
        
    @classmethod
    def get_id(cls, id):
        '''method to find a user by id'''
        try:
            format_str = f"""SELECT * FROM \"user\" WHERE id = {id}  LIMIT 1
                        """
            cursor.execute(format_str)
            retrieved_user = list(cursor.fetchone())
            user = UserModel(id=retrieved_user[0], name=retrieved_user[1], username=retrieved_user[2], email=retrieved_user[3], street=retrieved_user[4], suite=retrieved_user[5], city=retrieved_user[6], zipcode=retrieved_user[7], lat=retrieved_user[8],lng=retrieved_user[9], phone=retrieved_user[10],website=retrieved_user[11], company_name=retrieved_user[12],catchPhrase=retrieved_user[13], bs=retrieved_user[14], user_role=retrieved_user[15], personPic=retrieved_user[16], date_created=retrieved_user[17])

            return user.id
        except Exception as e:
            return {"error": e}
        
    @classmethod
    def get_all(cls):
        
        ''' method to get all users'''
        cursor.execute(
            f"SELECT * FROM public.user"
        )
        rows = cursor.fetchall()
        
        output = []
        
        for row in rows:
            new = UserModel(id=row[0], name=row[1], username=row[2], email=row[3], street=row[4], suite=row[5], city=row[6], zipcode=row[7], lat=row[8],lng=row[9], phone=row[10],website=row[11], company_name=row[12],catchPhrase=row[13], bs=row[14], user_role=row[15],  personPic=row[16], date_created=row[17])
            
            output.append(new.json_dumps())
            
        return output
    
    @classmethod
    def update(cls, user_role, id):
        """Method to update an user_role"""
        format_str = f"""
         UPDATE public.user SET user_role = '{user_role}' WHERE id = {id};
         """

        cursor.execute(format_str)

        return {
            "user_role": user_role
        }
        