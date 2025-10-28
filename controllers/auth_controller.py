# controllers/auth_controller.py

from flask import Blueprint, request, jsonify, current_app

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    
    try:
        data = request.json
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400

        
        

        
        if username == VALID_USERNAME:
            
           
            if password == VALID_PASSWORD:
                # Both are correct
                current_app.logger.info(f"Login successful for user: {username}")
                return jsonify({
                    "message": "Login successful"
                }), 200
            else:
                
                current_app.logger.warning(f"Wrong password for user: {username}")
                return jsonify({
                    "message": "Wrong password"
                }), 401
        
        else:
           
            current_app.logger.warning(f"Failed login attempt. User not found: {username}")
            return jsonify({
                "message": "Username not found"
            }), 401


    except Exception as e:
        current_app.logger.error(f"Error during login: {e}")
        return jsonify({"message": "An internal error occurred"}), 500