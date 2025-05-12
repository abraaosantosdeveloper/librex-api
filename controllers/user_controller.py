# user controller
from flask import Blueprint, jsonify, request
from workers.user_worker import ban_user_service, get_user_profile_service, register_user_service

user_bp = Blueprint('user', __name__)

@user_bp.route('/ban_user/<int:user_id>', methods=["POST", "OPTIONS"])
def ban_user(user_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    result, status_code = ban_user_service(user_id)
    return jsonify(result), status_code

@user_bp.route('/profile', methods=["GET"])
def get_user_profile():    
    # Pegar o token do cabeçalho da requisição
    auth_header = request.headers.get('Authorization')
    token = auth_header
    
    result, status_code = get_user_profile_service(token)
    return jsonify(result), status_code

@user_bp.route('/register', methods=["POST", "OPTIONS"])
def register_user():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    try:
        # Receber os dados do formulário de cadastro
        data = request.get_json()
        
        fname = data.get('fname')
        sname = data.get('sname')
        bdate = data.get('bdate')
        email = data.get('email')
        password = data.get('password')
        displayname = data.get('displayname')
        
        # Validação básica dos campos obrigatórios
        if not all([fname, sname, email, password, displayname]):
            return jsonify({"error": "Todos os campos são obrigatórios, exceto data de nascimento"}), 400
        
        result, status_code = register_user_service(fname, sname, bdate, email, password, displayname)
        return jsonify(result), status_code
    except Exception as e:
        print(f"Erro no controller de registro: {str(e)}")
        return jsonify({"error": f"Erro no processamento da solicitação: {str(e)}"}), 500
