# auth controller
from flask import Blueprint, request, jsonify
from workers.auth_worker import login_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["POST", "OPTIONS"])
def login_user():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    data = request.get_json()
    return login_service(data)

@auth_bp.route('/signup', methods=["POST", "OPTIONS"])
def signup_user():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    data = request.get_json()
    return jsonify({"message": "Funcionalidade em desenvolvimento"}), 501