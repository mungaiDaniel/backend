from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, make_response, jsonify, request
from app.users.model import UserModel
from flask_cors import cross_origin
import datetime

user_v1 = Blueprint('user-v1', __name__, url_prefix='/api/v1')

@user_v1.route('/register', methods=['POST'])
def post():
    data = request.get_json()

    name = data['name']
    username = data['username']
    email = data['email']
    # if UserModel.find_by_username(data['username']):
    #         return {'message': 'This username is already taken,kindly try another username'}, 409
    street= data["address"]["street"]
    suite = data["address"]["suite"]
    city = data["address"]["city"]
    zipcode =UserModel.generate_hash(data["address"]["zipcode"])
    lat = data["address"]["geo"]["lat"]
    lng = data["address"]["geo"]["lng"]
    phone = data["phone"]
    website = data["website"]
    company_name = data["company"]["company_name"]
    catchPhrase = data["company"]["catchPhrase"]
    bs = data["company"]["bs"]
    user_role= "user"
    personPic=data["personPic"]


    new_user = UserModel(id=None, name=name, username=username, email=email, street=street, suite=suite, city=city, zipcode=zipcode, lat=lat,lng=lng, phone=phone,website=website, company_name=company_name,catchPhrase=catchPhrase, bs=bs, user_role=user_role, personPic=personPic, date_created=datetime.datetime.now())


    new_user.save( name=name, username=username, email=email, street=street, suite=suite, city=city, zipcode=zipcode, lat=lat,lng=lng, phone=phone,website=website, company_name=company_name,catchPhrase=catchPhrase, bs=bs, user_role=user_role, personPic=personPic, date_created=datetime.datetime.now())

    return make_response(jsonify({ 
        "status": 201,
        "data": new_user.json_dumps()
    }), 201)

@user_v1.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'username {} doesnt exist'.format(data['username'])}, 404

        zipcode = data['zipcode']
        hash = current_user[7]

        if not UserModel.verify_hash(zipcode, hash):
            return {"message": "Incorrect password"}, 401
        
        user = UserModel(*current_user)

        # Assuming the user type is stored at index 15 of the user object
        if user.user_role == 'premium':
            permission_level = 1
        else:
            permission_level = 0

        token = user.generate_auth_token(permission_level)

        return jsonify({'token': token, "user_role": user.user_role, "id": user.id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_v1.route('/user', methods=['GET'])
def get_all_users():
    users = UserModel.get_all()

    return make_response(jsonify({
        "status": 200,
        "data": users
    }), 200)

@user_v1.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user = UserModel.find_by_id(id)

    return make_response(jsonify({
        "status": 200,
        "data": user
    }), 200)

@user_v1.route('/premium', methods=['PUT'])
@jwt_required()
def update_tO_premium():
    user_role = request.get_json()

    user_id = get_jwt_identity()

    user = UserModel.update(user_role=user_role['user_role'] , id=user_id)

    return make_response(jsonify({
        "status": 200,
        "data": user
    }), 200)


    
      


            


