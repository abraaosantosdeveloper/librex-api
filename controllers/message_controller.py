# message_controller.py
from flask import Blueprint, jsonify, request
from workers.message_worker import create_message, get_messages_for_user

message_bp = Blueprint('message', __name__)

@message_bp.route('/', methods=["POST", "OPTIONS"])
def add_message():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    data = request.json
    result, status_code = create_message(data)
    return jsonify(result), status_code

@message_bp.route('/user/<int:user_id>', methods=["GET", "OPTIONS"])
def get_user_messages(user_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    messages, status_code = get_messages_for_user(user_id)
    return jsonify(messages), status_code