from flask import Blueprint, jsonify, request
from app.models import User, Movie
from app import db
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

# TOKEN GENERATION

@api_bp.route("/token", methods=["POST"])
def get_token():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if user is None or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token})

# TOKEN VALIDATION DECORATOR

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            request.user = User.query.get(payload["user_id"])
        except:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# GET ALL MOVIES
@api_bp.route("/movies", methods=["GET"])
@token_required
def api_get_movies():
    movies = Movie.query.all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "year": m.year,
            "oscars": m.oscars,
            "genre": m.genre
        }
        for m in movies
    ])

# CREATE MOVIE

@api_bp.route("/movies", methods=["POST"])
@token_required
def api_add_movie():
    data = request.json
    movie = Movie(
        name=data["name"],
        year=data["year"],
        oscars=data["oscars"],
        genre=data.get("genre")
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({"message": "Movie added", "id": movie.id}), 201
