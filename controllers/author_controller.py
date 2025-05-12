from flask import Blueprint, jsonify, request
from repositories.author_repository import get_all_authors

author_bp = Blueprint("author", __name__)

@author_bp.route("/", methods=["GET", "OPTIONS"])
def get_authors():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    authors = get_all_authors()
    return jsonify(authors)