import csv
from .data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a list of all users
        pass

    def get_user_movies(self, user_id):
        pass
        # Return a list of all movies

    def update_user_movie(self, user_id, movie_id, updated_movie):
        pass
