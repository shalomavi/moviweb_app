from flask import Blueprint, jsonify, request
from data_manager.sqlite_data_manager import SQLiteDataManager
from moviweb_app.data_models.data_models import db

api = Blueprint('api', __name__)

data_manger = SQLiteDataManager(db)


@api.route('/users', methods=['GET'])
def list_users():
    users = data_manger.get_all_users()
    users_list = [{"user_name": user.name, "user_id": user.user_id} for user in users]
    return jsonify(users_list)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user_movies = data_manger.get_user_movies(user_id)
    user_movies_list = [{'movie_id': movie.movie_id, 'title': movie.title} for movie in user_movies]
    return jsonify(user_movies_list)


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    if data_manger.get_user_by_id(user_id):
        title = request.json.get('title')
        director = request.json.get('director')
        year = request.json.get('year')
        rating = request.json.get('rating')
        poster = request.json.get('poster')
        address = request.json.get('address')
        new_movie = {
            "title": title,
            "director": director,
            "year": str(year),
            "rating": str(rating),
            "poster": poster,
            "address": address,
        }
        data_manger.add_movie(user_id, new_movie)
        return jsonify({'message': 'Movie added successfully', 'movie_title': title}), 201
    return jsonify({"message": "User not found!"}), 400
