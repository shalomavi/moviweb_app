from sqlalchemy import and_
from .data_manager_interface import DataManagerInterface
from moviweb_app.data_models.data_models import User, Movie, Review
import requests

API_KEY = "87c55f08"


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        """
        initiate a db from data models
        :param db:
        """
        self.db = db

    def get_all_users(self):
        """
        gets all user in db
        :return:
        """
        try:
            return User.query.all()
        except Exception:
            print("no users in database")
            return []

    def get_user_movies(self, user_id):
        """
        get movies of a given user
        :param user_id:
        :return user.movies:
        """
        user = self.db.session.query(User).filter(User.user_id == user_id).one()
        if user:
            return user.movies
        return []

    def add_user(self, new_user):
        """
        adds users to all users list
        :param new_user:
        :return new_user:
        """
        user_to_add = new_user
        self.db.session.add(user_to_add)
        self.db.session.commit()
        return new_user

    def update_user_movie(self, user_id, movie_id, updated_movie):
        """
        updates a movie of given user
        :param user_id:
        :param movie_id:
        :param updated_movie:
        :return:
        """
        movie = Movie.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        year = int(updated_movie["year"]) if updated_movie["year"].isdigit() else None
        rating = float(updated_movie["rating"]) if \
            updated_movie["rating"].replace(".", "", 1).isdigit() else None

        if movie:
            movie.title = updated_movie['title']
            movie.director = updated_movie['director']
            movie.year = year
            movie.rating = rating
            self.db.session.commit()

    @staticmethod
    def row_to_dict(row):
        """
        converts a db row to dict
        :param row:
        :return:
        """
        dictionary = {}
        for column in row.__table__.columns:
            dictionary[column.name] = getattr(row, column.name)

        return dictionary

    def get_user_by_id(self, user_id):
        """
        get a user data by given id
        :param user_id:
        :return user_dict:
        """
        user = self.db.session.query(User).get(user_id)
        if user:
            return self.row_to_dict(user)

    def get_movie_by_id(self, user_id, movie_id):
        """
        returns a movie dict by given id.
        :param user_id:
        :param movie_id:
        :return movie:
        """
        movie = self.db.session.query(Movie).filter(Movie.movie_id == movie_id).one()
        if movie:
            return movie

    def get_user_name_by_id(self, user_id):
        return self.get_user_by_id(user_id)["name"]

    def register(self, user_id, username, password):
        """
        adds username and password to user.
        :param username:
        :param password:
        :param user_id:
        :return:
        """
        try:
            user = self.db.session.query(User).filter(User.user_id == user_id).one()
        except Exception:
            user = None
        try:
            another_user = self.db.session.query(User).filter(User.username == username).one()
        except Exception:
            another_user = None

        if another_user:
            return None
        if user:
            user.is_logged_in = True
            user.username = username
            user.password = password
            self.db.session.commit()

    def login(self, username, password, user_id):
        try:
            user = self.db.session.query(User).filter(User.user_id == user_id,
                                                      User.username == username).one()
        except Exception as e:
            print("Error retrieving user:", e)
            return None

        if user:
            print("Retrieved user:", user.username, user.username)
            print("actual pass:", user.password, password)
            if password == user.password:
                user.is_logged_in = True
                self.db.session.commit()
                return self.row_to_dict(user)
            else:
                print("Password doesn't match")
        else:
            print("User not found")

        return None

    def reset_logged_in(self):
        """
        resets all user logged in to False
        :return None:
        """
        all_users = self.get_all_users()
        for user in all_users:
            user.is_logged_in = False
            self.db.session.commit()

    def update_user(self, user_id, new_name):
        """
        gets new name and updates user.
        :param user_id:
        :param new_name:
        :return user:
        """
        user = self.db.session.query(User).filter(User.user_id == user_id).one()
        if user:
            user.name = new_name
            self.db.session.commit()
            return user
        return None

    def delete_user(self, user_id):
        """
        deletes user by its id.
        :param user_id:
        :return deleted user:
        """
        user = self.get_user_by_id(user_id)
        self.db.session.query(User).filter(User.user_id == user_id).delete()
        self.db.session.commit()
        return user

    def add_movie(self, user_id, new_movie):
        """
        adds a movie to users movie list.
        :param user_id:
        :param new_movie:
        :return new_movie:
        """
        year = int(new_movie["year"]) if new_movie["year"].isdigit() else None
        rating = float(new_movie["rating"]) if \
            new_movie["rating"].replace(".", "", 1).isdigit() else None

        movie_to_add = Movie(title=new_movie["title"],
                             user_id=user_id,
                             director=new_movie["director"],
                             year=year,
                             rating=rating,
                             poster=new_movie["poster"],
                             address=new_movie["address"]
                             )
        self.db.session.add(movie_to_add)
        self.db.session.commit()
        return new_movie

    def delete_movie(self, user_id, movie_id):
        """
        deletes movie by its id.
        :param user_id:
        :param movie_id:
        :return deleted user:
        """
        movie = self.get_movie_by_id(user_id, movie_id)
        self.db.session.query(Movie).filter(Movie.movie_id == movie_id
                                            and Movie.user_id == user_id).delete()
        self.db.session.commit()
        return movie

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

        new_movie_id = None
        no_img_url = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
        poster = no_img_url
        address = ""
        new_movie["movie_id"] = new_movie_id
        new_movie["poster"] = poster
        new_movie["address"] = address
        return new_movie

    def generate_movie_id(self, user_id):
        """
        generates a max number + 1, in movies ids.
        :param user_id:
        :return movie_id:
        """
        # user_movies = self.get_user_movies(user_id)
        # if not user_movies:
        #     return 1
        # return max([movie["movie_id"] for movie in user_movies]) + 1
        return

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
    def generate_user_id(users):
        """
        function just returns none due to compatibility
         with other data managers adjustments.
        :param users:
        :return user_id:
        """
        # if not users:
        #     return 1
        # return max([user["user_id"] for user in users]) + 1
        return

    def create_user_details(self, user_id, name):
        """
        gets new user details data
         and returns a dict of user
        :param user_id:
        :param name:
        :return new_user:
        """
        user_to_add = User(name=name)
        self.db.session.add(user_to_add)
        self.db.session.commit()
        return user_to_add

    def add_review(self, user_id, movie_id, review):
        """
        gets new user details data
         and returns a review of user
        :param user_id:
        :param movie_id:
        :param review:
        :return review_to_add:
        """
        review_to_add = Review(user_id=user_id, movie_id=movie_id, review=review)
        self.db.session.add(review_to_add)
        self.db.session.commit()
        return review_to_add

    def get_reviews(self, user_id, movie_id):
        """
        get all reviews of a movie from  db
        :param user_id:
        :param movie_id:
        :return reviews:
        """
        reviews = self.db.session.query(Review).filter(
            and_(Review.movie_id == movie_id, Review.user_id == user_id)
        ).all()
        if reviews:
            return reviews

    def delete_review(self, user_id, movie_id, review_id):
        """
        deletes a review  from db
        :param user_id:
        :param movie_id:
        :param review_id:
        :return None:
        """
        self.db.session.query(Review).filter(
            and_(Review.movie_id == movie_id, Review.user_id == user_id, Review.review_id == review_id)
        ).delete()
        self.db.session.commit()
