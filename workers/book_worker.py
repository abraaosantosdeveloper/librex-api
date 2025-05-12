#book_worker.py
from repositories.book_repository import *
import traceback
# Correção para book_worker.py
# Problema: A verificação de erro na função create_book está incorreta

def create_book(book_data):
    try:
        if not isinstance(book_data, dict):
            return {"error": "Formato de dados inválido. Esperado um JSON (objeto)."}, 400

        print(f"Dados recebidos: {book_data}")
        
        required_fields = ['title', 'synopsis', 'author_id', 'genre_id', 'user_id']
        missing_fields = [field for field in required_fields if field not in book_data or book_data[field] is None]
        
        if missing_fields:
            return {"error": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"}, 400

        # Converter os IDs para inteiros para garantir compatibilidade
        for id_field in ['author_id', 'genre_id', 'user_id']:
            try:
                book_data[id_field] = int(book_data[id_field])
            except (ValueError, TypeError):
                return {"error": f"O campo {id_field} deve ser um número inteiro válido"}, 400
        
        # Converter pages para inteiro ou None
        if 'pages' in book_data and book_data['pages']:
            try:
                book_data['pages'] = int(book_data['pages'])
            except (ValueError, TypeError):
                return {"error": "O campo 'pages' deve ser um número inteiro válido"}, 400

        book_id, db_error = add_book_to_db(book_data)
        
        if db_error:  # Se há erro, db_error não será None
            return {"error": f"Erro ao adicionar livro ao banco de dados: {db_error}"}, 500

        return {"id": book_id}, 201

    except Exception as e:
        error_message = str(e) or "Erro desconhecido ao adicionar livro"
        print(f"Erro detalhado: {error_message}")
        print(traceback.format_exc())
        return {"error": error_message}, 500

def get_all_books(user_id=None):
    """
    Obtém todos os livros, incluindo status de favorito se um user_id for fornecido.
    """
    try:
        return get_all_books_from_db(user_id)
    except Exception as e:
        print(f"Erro ao buscar livros: {e}")
        traceback.print_exc()
        return []

def get_all_evaluations(book_id=None):
    try:
        return get_evaluations_from_db(book_id)
    except Exception as e:
        print(f"Erro ao buscar comentários: {e}")
        traceback.print_exc()
        return []

def toggle_book_favorite(user_id, book_id):
    """
    Alterna o status de favorito de um livro para um usuário.
    """
    try:
        # Conversão para inteiros para garantir compatibilidade
        user_id = int(user_id)
        book_id = int(book_id)
        
        result = toggle_favorite(user_id, book_id)
        return result, 200
    except ValueError:
        return {"error": "IDs de usuário e livro devem ser números inteiros válidos"}, 400
    except Exception as e:
        error_message = str(e) or "Erro desconhecido ao alternar favorito"
        print(f"Erro detalhado: {error_message}")
        traceback.print_exc()
        return {"error": error_message}, 500


def delete_book_from_lib(book_id):
    try:
        # Conversão para inteiros para garantir compatibilidade
        book_id = int(book_id)
        
        result = delete_book(book_id)
        return result, 200
    except ValueError:
        return {"error": "IDs de usuário e livro devem ser números inteiros válidos"}, 400
    except Exception as e:
        error_message = str(e) or "Erro desconhecido ao Apagar"
        print(f"Erro detalhado: {error_message}")
        traceback.print_exc()
        return {"error": error_message}, 500
    
