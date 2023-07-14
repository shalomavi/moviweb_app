"""
json data manager module
"""
import json
import requests
from .data_manager_interface import DataManagerInterface

API_KEY = "87c55f08"


class JSONDataManager(DataManagerInterface):
    """
    json data manager to all users and their movies
    """

    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """
        gets all users data from csv file.
        :return data:
        """
        # Return a list of all users
        try:
            with open(self.filename) as handle:
                data = json.loads(handle.read())
            return data

        except Exception as error:
            return error

    def add_user(self, new_user):
        """
        adds users to all users list
        :param new_user:
        :return all_users:
        """
        all_users = self.get_all_users()
        all_users.append(new_user)
        self.update_file(all_users)
        return all_users

    def get_user_by_id(self, user_id):
        """
        returns user movies list by given id.
        :param user_id:
        :return user:
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user["user_id"] == user_id:
                return user
        return None

    def update_user(self, user_id, new_name):
        """
        gets new name and updates user.
        :param user_id:
        :param new_name:
        :return user:
        """
        all_user = self.get_all_users()
        for user in all_user:
            if user["user_id"] == user_id:
                user["name"] = new_name
                self.update_file(all_user)
                return user
        return None

    def delete_user(self, user_id):
        """
        deletes user by its id.
        :param user_id:
        :return deleted_user:
        """
        all_users = self.get_all_users()
        temp_users = []
        deleted_user = None
        for user in all_users:
            if user["user_id"] != user_id:
                temp_users.append(user)
            else:
                deleted_user = user
        self.update_file(temp_users)
        return deleted_user

    def get_user_movies(self, user_id):
        """
        returns a list of movies of user by given id.
        :param user_id:
        :return user_movies:
        """
        # Return a list of all movies for a given user
        all_users = self.get_all_users()
        for user in all_users:
            if user["user_id"] == user_id:
                return user["movies"]
        return None

    def get_movie_by_id(self, user_id, movie_id):
        """
        returns a movie dict by given id.
        :param user_id:
        :param movie_id:
        :return movie:
        """
        movies = self.get_user_movies(user_id)
        for movie in movies:
            if movie["movie_id"] == movie_id:
                return movie
        return None

    def get_user_name_by_id(self, user_id):
        """
        returns user by its id.
        :param user_id:
        :return user name:
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user["user_id"] == user_id:
                return user["name"]
        return None

    def add_movie(self, user_id, new_movie):
        """
        adds a movie to users movie list.
        :param user_id:
        :param new_movie:
        :return new_movie:
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user["user_id"] == user_id:
                user["movies"].append(new_movie)
        self.update_file(all_users)
        return new_movie

    def get_api_data_to_dict(self, api_data, new_movie_id):
        """
        gets api data and returns a list of dicts
        :param api_data:
        :param new_movie_id:
        :return new_movie:
        """
        title = api_data.get('Title')
        year = api_data.get('Year')
        rating = api_data.get('imdbRating')
        director = api_data.get('Director')
        poster = api_data.get('Poster')
        address = self.get_movie_website_address(title)
        new_movie = {
            "movie_id": new_movie_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating,
            "poster": poster,
            "address": address
        }

        return new_movie

    @staticmethod
    def get_movies_api(title):
        """
        connect to omdbapi and gets the api for the selected
        title and return a dictionary of the movie data
        :param title:
        :return dict_of_movie_data:
        """
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        try:
            res = requests.get(url)
        except Exception as error:
            print(f"{error}\n Check connections!")
            return None
        data = res.json()
        return data

    def get_movie_website_address(self, title):
        """
        gets data of a movie and returns its imdb address
        :param title:
        :return address:
        """
        imdb_id = self.get_movies_api(title).get('imdbID')
        if imdb_id is None:
            return None
        address = f'https://www.imdb.com/title/{imdb_id}/'
        return address

    @staticmethod
    def form_data_to_form_objects_dict(form_items):
        """
        loops through data and returns as dict
        :param form_items:
        :return form_data_dict:
        """
        form_data_dict = {}
        for key, val in form_items:
            form_items[key] = val
        return form_data_dict

    def convert_form_data_to_new_movie_dict(self, form_objects_dict, user_id):
        """
        converts form data to a dict.
        :param form_objects_dict:
        :param user_id:
        :return new_movie:
        """
        new_movie = {}
        for key, val in form_objects_dict.items():
            new_movie[key] = val

        new_movie_id = self.generate_movie_id(user_id)
        no_img_url = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
        poster = no_img_url
        address = ""
        new_movie["movie_id"] = new_movie_id
        new_movie["poster"] = poster
        new_movie["address"] = address

        return new_movie

    def delete_movie(self, user_id, movie_id):
        """
        deletes movie from users data by id.
        :param user_id:
        :param movie_id:
        :return deleted_movie:
        """
        movies = self.get_user_movies(user_id)
        temp_movies = []
        deleted_movie = None
        try:
            for movie in movies:
                if movie["movie_id"] != movie_id:
                    temp_movies.append(movie)
                else:
                    deleted_movie = movie
            self.add_new_movie_list(temp_movies, user_id)
            return deleted_movie
        except TypeError as error:
            print("user id invalid! ", error)
        return None

    def add_new_movie_list(self, movies_list, user_id):
        """
        adds a new movie to users list of movies.
        :param movies_list:
        :param user_id:
        :return movies_list:
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user['user_id'] == user_id:
                user['movies'] = movies_list
        self.update_file(all_users)
        return movies_list

    def update_user_movie(self, user_id, movie_id, updated_movie):
        """
        updates a movie of user by its id.
        :param user_id:
        :param movie_id:
        :param updated_movie:
        :return updated_movie:
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user["user_id"] == user_id:
                for movie in user["movies"]:
                    if movie["movie_id"] == movie_id:
                        movie.update(updated_movie)
        self.update_file(all_users)
        return updated_movie

    @staticmethod
    def generate_user_id(users):
        """
        generates a max number + 1, in users ids.
        :param users:
        :return user_id:
        """
        if not users:
            return 1
        return max([user["user_id"] for user in users]) + 1

    def generate_movie_id(self, user_id):
        """
        generates a max number + 1, in movies ids.
        :param user_id:
        :return movie_id:
        """
        user_movies = self.get_user_movies(user_id)
        if not user_movies:
            return 1
        return max([movie["movie_id"] for movie in user_movies]) + 1

    def update_file(self, data_file):
        """
        updates the data.json file.
        :param data_file:
        :return None:
        """
        try:
            with open(self.filename, "w") as handle:
                handle.write(json.dumps(data_file, indent=4))
        except IOError as error:
            print("An IOError occurred: ", str(error))
