# message_repository.py
from connector import executeDictQuery, executeCommand

def add_message_to_db(message_data):
    query = """
    INSERT INTO messages (sender_id, recipient_id, title, content)
    VALUES (%s, %s, %s, %s)
    """
    
    params = (
        message_data['sender_id'],
        message_data['recipient_id'],
        message_data['title'],
        message_data['content']
    )
    
    message_id = executeCommand(query, params)
    return message_id

def get_messages_for_user_from_db(user_id):
    # Query com JOIN para buscar o nome do remetente e formatação da data
    query = """
    SELECT 
        m.id, 
        m.sender_id, 
        u.username as sender_name, 
        m.title, 
        m.content, 
        DATE_FORMAT(m.created_at, '%d/%m/%Y - %H:%i') as formatted_date,
        m.created_at
    FROM messages m
    JOIN users u ON m.sender_id = u.id
    WHERE m.recipient_id = %s
    ORDER BY m.created_at DESC
    """
    
    messages = executeDictQuery(query, (user_id,))
    return messages

def get_admin_ids_from_db():
    query = "SELECT id FROM users WHERE admin = 1"
    admin_users = executeDictQuery(query)
    return [admin['id'] for admin in admin_users]