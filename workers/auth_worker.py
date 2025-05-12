# auth worker
import jwt
from config import SECRET_KEY
from encode import verify_password
from repositories.user_repository import find_user_by_email
from cryptography.fernet import Fernet

def login_service(data):
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return {"error": "Todos os campos obrigatórios!"}, 400
    
    try:
        user = find_user_by_email(email)
        
        if not user:
            return {"error": "Credenciais inválidas."}, 401  

        user_id, user_email, hashed_password, is_admin = user
        
        if not verify_password(password, hashed_password):
            return {"error": "Credenciais inválidas."}, 401
        
        token = jwt.encode({'user_id': user_id, 'email': user_email}, SECRET_KEY, algorithm='HS256')
        
        fernet = Fernet(SECRET_KEY)
        token = fernet.encrypt(token.encode()).decode()

        return {
            "message": "Login realizado com sucesso!",
            "token": token,
            "admin": is_admin,
            "userId": user_id
        }
        
    except Exception as e:
        print("Erro ao realizar login:", str(e))
        return {"error": "Erro interno do servidor."}