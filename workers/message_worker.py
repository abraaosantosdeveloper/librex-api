# message worker
from repositories.message_repository import add_message_to_db, get_messages_for_user_from_db, get_admin_ids_from_db

def create_message(message_data):
    try:
        # Validar dados da mensagem
        required_fields = ['sender_id', 'recipient_id', 'title', 'content']
        for field in required_fields:
            if field not in message_data:
                return {"error": f"Campo obrigatório ausente: {field}"}, 400
        
        # Adicionar mensagem ao banco de dados
        message_id = add_message_to_db(message_data)
        
        if message_id:
            return {"message": "Mensagem enviada com sucesso", "id": message_id}, 201
        else:
            return {"error": "Erro ao enviar mensagem"}, 500
    
    except Exception as e:
        return {"error": str(e)}, 500

def get_messages_for_user(user_id):
    try:
        # Buscar mensagens do usuário
        messages = get_messages_for_user_from_db(user_id)
        return messages, 200
    
    except Exception as e:
        return {"error": str(e)}, 500

def notify_admins_about_new_book(book_id, book_title, user_id):
    """
    Envia uma mensagem para todos os administradores notificando sobre um novo livro
    que precisa de aprovação.
    """
    try:
        # Obter IDs de todos os administradores
        admin_ids = get_admin_ids_from_db()
        
        if not admin_ids:
            return False, "Nenhum administrador encontrado"
        
        # Preparar dados da mensagem
        message_data = {
            'sender_id': user_id,  # O próprio usuário é o remetente
            'title': 'Novo livro para aprovação',
            'content': f'Um novo livro "{book_title}" (ID {book_id}) foi enviado para aprovação.'
        }
        
        # Enviar mensagem para cada administrador
        success_count = 0
        for admin_id in admin_ids:
            message_data['recipient_id'] = admin_id
            message_id = add_message_to_db(message_data)
            if message_id:
                success_count += 1
        
        if success_count > 0:
            return True, f"Notificação enviada para {success_count} administradores"
        else:
            return False, "Falha ao notificar administradores"
    
    except Exception as e:
        return False, str(e)