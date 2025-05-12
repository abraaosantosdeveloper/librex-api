#book_controller.py
from flask import Blueprint, jsonify, request
from workers.book_worker import *
import jwt
from config import SECRET_KEY
from cryptography.fernet import Fernet

book_bp = Blueprint('book', __name__)

@book_bp.route('/', methods=["GET", "OPTIONS"])
def get_books():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    books = get_all_books_from_db()
    return jsonify(books), 200

@book_bp.route('/', methods=["POST", "OPTIONS"])
def add_book():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({'error': 'Requisição deve ser JSON válido com Content-Type: application/json'}), 400

    result, status_code = create_book(data)
    return jsonify(result), status_code

@book_bp.route('/favorite/<int:book_id>', methods=["POST", "OPTIONS"])
def toggle_favorite(book_id):
    """
    Endpoint para alternar o status de favorito de um livro.
    """
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    # Obtenha o ID do usuário atual da sessão ou token
    # Esta é uma implementação de exemplo - adapte conforme seu sistema de autenticação
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
        
    result, status_code = toggle_book_favorite(user_id, book_id)
    return jsonify(result), status_code



# Função auxiliar para obter o ID do usuário atual
def get_current_user_id():
    """
    Obtém o ID do usuário atual com base no sistema de autenticação.
    Adapte esta função de acordo com seu sistema de autenticação.
    """
    auth_header = request.headers.get('Authorization')
    token = auth_header
    if token and token.startswith('Bearer '):
         token = auth_header.split(' ')[1]
    fernet = Fernet(SECRET_KEY)
    decriptedToken = fernet.decrypt(token)
    decodedToken = jwt.decode(decriptedToken, SECRET_KEY, ['HS256'])
    user_id = decodedToken["user_id"]
    return user_id

@book_bp.route('/favorites/list', methods=["GET"])
def list_favorites():
    """
    Endpoint para retornar apenas os IDs dos livros favoritos do usuário atual.
    """
    # Obtenha o ID do usuário atual da sessão ou token
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
    
    try:
        # Query para buscar apenas os IDs dos livros favoritos
        query = "SELECT book_id FROM favorites WHERE user_id = %s"
        favorites = executeDictQuery(query, (user_id,))
        
        # Extrair apenas os IDs dos livros
        favorite_ids = [fav['book_id'] for fav in favorites]
        
        return jsonify({"favorites": favorite_ids}), 200
        
    except Exception as e:
        print(f"Erro ao listar favoritos: {str(e)}")
        return jsonify({"error": "Erro ao buscar favoritos", "message": str(e)}), 500
    

@book_bp.route('/delete/<int:book_id>', methods=["DELETE", "OPTIONS"])
def delete_book(book_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    # Obtenha o ID do usuário atual da sessão ou token
    # Esta é uma implementação de exemplo - adapte conforme seu sistema de autenticação
    user_id = get_current_user_id()
    
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401
        
    result, status_code = delete_book_from_lib(book_id)
    return jsonify(result), status_code

@book_bp.route('/evaluations/<int:book_id>', methods=["GET"])
def get_book_evaluations(book_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    evaluations = get_all_evaluations(book_id)
    return jsonify(evaluations), 200