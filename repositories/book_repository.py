# book repository
from connector import *

def get_book_by_id(book_id):
    query = "SELECT * FROM books WHERE id = %s"
    result = executeDictQuery(query, (book_id,))
    
    if not result:
        return None
    
    return result[0]

# Correção para book_repository.py
# Problema: A função add_book_to_db está retornando valores inconsistentes

def add_book_to_db(book_data):
    query = """
    INSERT INTO books (title, synopsis, author_id, genre_id, user_id, pages)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    params = (
        book_data['title'],
        book_data['synopsis'],
        book_data['author_id'],
        book_data['genre_id'],
        book_data['user_id'],
        book_data.get('pages', None)  # Usa None se 'pages' não existir
    )
    
    try:
        book_id = executeCommand(query, params)
        return book_id, None  # Retorna o ID do livro e None para erro
    except Exception as e:
        print(f"Erro na inserção do livro: {str(e)}")
        return None, str(e)  # Retorna None para o ID e a mensagem de erro



def is_admin(user_id):
    query = "SELECT admin FROM users WHERE id = %s"
    result = executeDictQuery(query, (user_id,))
    
    if not result:
        return False
    
    return result[0]['admin'] == 1

def get_all_books_from_db(user_id=None):
    """
    Obtém todos os livros do banco de dados com informação de favorito
    para o usuário especificado.
    """
    if user_id is None:
        user_id = 0  # Valor padrão para quando não houver usuário logado  
    
    query = """
    SELECT b.id as book_id, b.title, a.name as author, b.synopsis, g.genre as genre, 
        IF(f.book_id IS NOT NULL, TRUE, FALSE) as favorite
    FROM books b
    JOIN authors a ON b.author_id = a.id
    JOIN genres g ON b.genre_id = g.id
    LEFT JOIN favorites f ON b.id = f.book_id AND f.user_id = %s
    ORDER BY b.created_at DESC
    """
    
    books = executeDictQuery(query, (user_id,))
    
    formatted_books = []
    for book in books:
        formatted_book = {
            'id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'synopsis': book['synopsis'],
            'genre': book['genre'],
            'favorite': bool(book['favorite'])
        }
        formatted_books.append(formatted_book)
        
    return formatted_books

def get_evaluations_from_db(book_id):
    if book_id is None:
        book_id = 0
    
    query = """
        SELECT 
            e.id AS evaluation_id,
            e.grade, 
            e.created_at, 
            c.comment,
            u.id AS user_id,
            u.displayname AS user_name
        FROM evaluations e 
        JOIN users u ON e.user_id = u.id
        LEFT JOIN comments c ON c.evaluation_id = e.id
        WHERE e.book_id = %s
        ORDER BY e.created_at DESC;
    """

    evaluations = executeDictQuery(query, (book_id,))

    formatted_evaluations = []
    for evaluation in evaluations:
        formatted_evaluation = {
            'id': evaluation['evaluation_id'],
            'rating': evaluation['grade'],
            'date': evaluation['created_at'],
            'username': evaluation['user_name'],
            'comment': evaluation['comment']

        }
        formatted_evaluations.append(formatted_evaluation)
    return formatted_evaluations
    

def toggle_favorite(user_id, book_id):
    """
    Adiciona ou remove um livro dos favoritos de um usuário.
    """
    # Verifica se já existe um favorito
    check_query = "SELECT book_id FROM favorites WHERE user_id = %s AND book_id = %s"
    existing = executeDictQuery(check_query, (user_id, book_id))
    
    if existing:
        # Se existe, remova
        delete_query = "DELETE FROM favorites WHERE user_id = %s AND book_id = %s"
        executeDictCommand(delete_query, (user_id, book_id))
        return {"favorite": False}
    else:
        # Se não existe, adicione
        insert_query = "INSERT INTO favorites (user_id, book_id) VALUES (%s, %s)"
        executeDictCommand(insert_query, (user_id, book_id))
        return {"favorite": True}

def delete_book(book_id):
    # Verifica se o livro existe
    check_query = "SELECT * FROM books WHERE id = %s"
    existing = executeDictQuery(check_query, (book_id,))
    
    if existing:
        # Se existe, remova
        delete_query = "DELETE FROM books WHERE id = %s"
        executeDictCommand(delete_query, (book_id,))
        return {"message": "Excluído com sucesso"}
    else:
        return {"message": "Livro não encontrado"}