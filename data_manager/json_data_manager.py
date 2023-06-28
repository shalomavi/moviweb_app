import json
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a list of all users
        with open(self.filename) as handle:
            data = json.loads(handle.read())
        return data

    def add_user(self, new_user):
        all_users = self.get_all_users()
        all_users.append(new_user)
        self.update_file(all_users)
        return all_users

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        all_users = self.get_all_users()
        for user in all_users:
            if user["id"] == user_id:
                return user["movies"]

    def get_movie_by_id(self, user_id, movie_id):
        movies = self.get_user_movies(user_id)
        for movie in movies:
            if movie["id"] == movie_id:
                return movie

    def get_user_name_by_id(self, user_id):
        all_users = self.get_all_users()
        for user in all_users:
            if user["id"] == user_id:
                return user["name"]

    def add_movie(self, user_id, new_movie):
        all_users = self.get_all_users()
        for user in all_users:
            if user["id"] == user_id:
                user["movies"].append(new_movie)
        self.update_file(all_users)
        return new_movie

    def delete_movie(self, user_id, movie_id):
        movies = self.get_user_movies(user_id)
        temp_movies = []
        deleted_movie = {}
        for movie in movies:
            if movie["id"] != movie_id:
                temp_movies.append(movie)
                deleted_movie = movie
        self.add_new_movie_list(temp_movies, user_id)
        return deleted_movie

    def add_new_movie_list(self, movies_list, user_id):
        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                user['movies'] = movies_list
        self.update_file(all_users)
        return movies_list

    def update_user_movie(self, user_id, movie_id, updated_movie):
        all_users = self.get_all_users()
        for user in all_users:
            if user["id"] == user_id:
                for movie in user["movies"]:
                    if movie["id"] == movie_id:
                        movie.update(updated_movie)
        self.update_file(all_users)
        return updated_movie

    def update_file(self, data_file):
        with open(self.filename, "w") as handle:
            handle.write(json.dumps(data_file))
