from flask import Blueprint, jsonify, request
from repositories.genre_repository import get_all_genres

genre_bp = Blueprint("genre", __name__)

@genre_bp.route("/", methods=["GET", "OPTIONS"])
def get_genders():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    genres = get_all_genres()
    return jsonify(genres)