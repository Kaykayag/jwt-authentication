
from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime


MOCK_USERS = [
    {
        "id": 1,
        "username": "admin",
        "password": "password123",
        "name": "Administrator",
        "role": "admin"
    },
    {
        "id": 2,
        "username": "user",
        "password": "password",
        "name": "Regular User",
        "role": "user"
    }
]

auth_bp = Blueprint('auth_bp', __name__)

def _find_user_by_username(username):
    """A helper function to find a user in our mock DB."""
    for user in MOCK_USERS:
        if user['username'] == username:
            return user
    return None

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles the login request.
    Validates credentials and returns user details and a JWT on success.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400

   
        user = _find_user_by_username(username)

        if not user:
            current_app.logger.warning(f"Failed login attempt. User not found: {username}")
            return jsonify({"message": "Username not found"}), 401
        
       
        if user['password'] != password:
        
            current_app.logger.warning(f"Wrong password for user: {username}")
            return jsonify({"message": "Wrong password"}), 401

      
        payload = {
            'sub': user['id'],  
            'name': user['name'],
            'role': user['role'],
            'iat': datetime.datetime.now(), 
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1) 
        }
        
        
        secret_key = current_app.config['SECRET_KEY']
        
        # token
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        

        user_details = {
            "id": user['id'],
            "username": user['username'],
            "name": user['name'],
            "role": user['role']
        }

        current_app.logger.info(f"Login successful for user: {username}")
        
      
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user_details
        }), 200

    except Exception as e:
        
        current_app.logger.error(f"Error during login for user {username}: {e}")
        return jsonify({"message": "An internal error occurred"}), 500