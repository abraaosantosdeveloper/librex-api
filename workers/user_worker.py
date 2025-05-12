# user worker
from repositories.user_repository import ban_user_by_id, get_user_by_id, find_user_by_email, register_user
import jwt
from config import SECRET_KEY
from cryptography.fernet import Fernet
from encode import hash_password, verify_password

def ban_user_service(user_id):
    try:
        ban_user_by_id(user_id)
        return {"message": f"Usuário {user_id} banido com sucesso"}, 200
    except Exception as e:
        return {"error": f"Erro ao banir usuário: {str(e)}"}, 500
    
def get_user_profile_service(token):
    try:
        # Decodificar o token JWT para obter o ID do usuário
        fernet = Fernet(SECRET_KEY)
        decriptedToken = fernet.decrypt(token)
        decoded = jwt.decode(decriptedToken, SECRET_KEY, ['HS256'])
        user_id = decoded.get('user_id')
        
        if not user_id:
            return {"error": "Token inválido"}, 401
        
        # Buscar os dados do usuário pelo ID
        user_data = get_user_by_id(user_id)
        
        if not user_data:
            return {"error": "Usuário não encontrado"}, 404
        
        # Converter para dicionário para facilitar a manipulação e JSON
        user_dict = {
            "id": user_data[0],
            "fname": user_data[1],
            "sname": user_data[2],
            "bdate": user_data[3].strftime('%d/%m/%Y') if user_data[3] else None,  # Formatando a data
            "username": user_data[4],
            "email": user_data[5]
        }
        
        return user_dict, 200
        
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}, 401
    except Exception as e:
        print(f"Erro ao buscar perfil: {str(e)}")
        return {"error": "Erro interno do servidor"}, 500

def register_user_service(fname, sname, bdate, email, password, displayname):
    try:
        # Verificar se o e-mail já está em uso
        existing_user = find_user_by_email(email)
        if existing_user:
            return {"error": "E-mail já cadastrado"}, 409
        
        # Hash da senha para armazenamento seguro
        hashed_password = hash_password(password)
        
        # Registrar o novo usuário
        user_id = register_user(fname, sname, bdate, email, hashed_password, displayname)
        
        if not user_id:
            return {"error": "Erro ao criar usuário"}, 500
            
        # Gerar token JWT para autenticação imediata
        token_payload = {"user_id": user_id[0]}
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        
        # Criptografar o token
        fernet = Fernet(SECRET_KEY)
        encrypted_token = fernet.encrypt(token.encode()).decode()
        
        # Determinar se é admin (todos os novos usuários são não-admin)
        is_admin = 0
        
        return {
            "message": "Usuário registrado com sucesso",
            "token": encrypted_token,
            "admin": is_admin
        }, 201
        
    except Exception as e:
        print(f"Erro ao registrar usuário: {str(e)}")
        return {"error": f"Erro ao registrar usuário: {str(e)}"}, 500