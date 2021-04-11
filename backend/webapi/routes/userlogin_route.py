from flask import Blueprint, request, jsonify, Response
from backend.repository.repository import UserLoginRepository
from backend.db.model import UserLogin

userlogin_routes = Blueprint('userlogin_routes', __name__, url_prefix='/user')

repository = UserLoginRepository()


# chrome://inspect/#devices for testing

@userlogin_routes.route('/get_userlogin', methods=['GET'])
def get_userlogin():
    """
    http://
    :return:
    """
    email = request.args.get('email')
    password = request.args.get('password')
    if email is None or password is None:
        return jsonify(({"error": "Missing request parameters"})), 400

    userlogin = repository.verify_userlogin(email=email, password=password)
    if userlogin is None:
        return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify(userlogin.serialize()), 200


@userlogin_routes.route('/add_userlogin', methods=['POST'])
def add_userlogin():
    data = request.get_json()

    email = data['email']
    password = data['password']

    repository.insert_userlogin(UserLogin(email=email, password=password))
    return "Success", 200

