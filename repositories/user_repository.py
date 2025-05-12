# user repository
from connector import executeSingleFetchQuery, executeDictQuery, executeCommand

def find_user_by_email(email):
    query = "SELECT id, email, password, admin FROM users WHERE email = %s"
    return executeSingleFetchQuery(query, (email,))

def ban_user_by_id(user_id):
    query = "UPDATE users SET banned = 1 WHERE id = %s"
    return executeDictQuery(query, (user_id,))

def get_user_by_id(user_id):
    query = """
    SELECT id, fname, sname, bdate, displayname, email 
    FROM users 
    WHERE id = %s AND banned = 0
    """
    return executeSingleFetchQuery(query, (user_id,))

def register_user(fname, sname, bdate, email, password, displayname):
    # Primeiro inserimos o usuário
    query = """
    INSERT INTO users (fname, sname, bdate, email, password, displayname, admin, banned)
    VALUES (%s, %s, %s, %s, %s, %s, 0, 0)
    """
    executeCommand(query, (fname, sname, bdate, email, password, displayname))
    
    # Depois buscamos o ID inserido pela consulta do email
    query_id = "SELECT id FROM users WHERE email = %s"
    return executeSingleFetchQuery(query_id, (email,))