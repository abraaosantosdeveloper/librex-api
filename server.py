# server
from flask import Flask, request
from flask_cors import CORS

from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.book_controller import book_bp
from controllers.author_controller import author_bp
from controllers.genre_controller import genre_bp
from controllers.message_controller import message_bp

app = Flask(__name__)

# Configuração CORS simplificada e robusta
CORS(app, 
     resources={r"/*": {
         "origins": "*",
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"]
     }})

# Tratamento explícito para requisições OPTIONS
@app.after_request
def after_request(response):
    if request.method == 'OPTIONS':
        response.status_code = 200
    return response

# Registro dos Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(book_bp, url_prefix='/books')
app.register_blueprint(author_bp, url_prefix='/authors')
app.register_blueprint(genre_bp, url_prefix='/genres')
app.register_blueprint(message_bp, url_prefix='/messages')
