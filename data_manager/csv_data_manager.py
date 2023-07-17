"""
csv data manager module
"""
import csv
from moviweb_app.data_manager.json_data_manager import JSONDataManager


class CSVDataManager(JSONDataManager):
    """
    csv data manager to all users and their movies.
     inherits most of its methods from JSONDataManager.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename

    @staticmethod
    def list_of_dicts_to_csv(list_of_dicts, csv_file):
        """
        converts data from list of dicts to csv, in csv file.
        :param list_of_dicts:
        :param csv_file:
        :return None:
        """
        data = list_of_dicts
        # Write the data to a CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['user_id', 'name', 'is_logged_in',
                             'movie_id', 'title',
                             'director', 'year',
                             'rating', 'poster',
                             'address', 'username', 'password'])
            # Write the data rows
            for item in data:
                user_id = item['user_id']
                name = item['name']
                logged_in = item['is_logged_in']
                movies = item['movies']
                username = item.get('username')
                password = item.get('password')
                for movie in movies:
                    movie_id = movie.get('movie_id', 00)
                    title = movie.get('title', "ADD Movies as you wish")
                    director = movie.get('director')
                    year = movie.get('year')
                    rating = movie.get('rating')
                    poster = movie.get('poster')
                    address = movie.get('address', f"/users/{user_id}/add_movie")
                    print(address)
                    writer.writerow([user_id, name, logged_in, movie_id,
                                     title, director, year,
                                     rating, poster, address,
                                     username, password])

        print(f"CSV file '{csv_file}' created successfully.")

    @staticmethod
    def change_csv_to_list_of_dicts(data):
        """
        converts csv data to list of dicts
        :param data:
        :return list_of_dicts:
        """
        list_of_dicts = []
        user_id = 0
        user_spot = -1

        for user in data[1:]:
            if user[2] == "False":
                is_logged = False
            else:
                is_logged = True

            user_dict = {
                "user_id": int(user[0]),
                "name": user[1],
                "is_logged_in": is_logged,
                "movies": [],
                "username": user[10],
                "password": user[11],
            }
            if user[2]:
                movie = {
                    "movie_id": int(user[3]),
                    "title": user[4],
                    "director": user[5],
                    "year": int(user[6]) if type(user[6]) == int else user[6],
                    "rating": float(user[7]) if type(user[7]) == float else user[7],
                    "poster": user[8],
                    "address": user[9]
                }
            else:
                movie = {}
            if int(user[0]) == user_id:
                list_of_dicts[user_spot]["movies"].append(movie)

            else:
                list_of_dicts.append(user_dict)
                user_spot += 1
                list_of_dicts[user_spot]["movies"].append(movie)
                user_id = int(user[0])

        return list_of_dicts

    def get_all_users(self):
        """
        returns a list of dicts of all users
        :return lists_of_dicts_data:
        """
        # Return a list of all users
        with open(self.filename, newline='') as handle:
            reader = csv.reader(handle)
            data = list(reader)
        lists_of_dicts_data = self.change_csv_to_list_of_dicts(data)
        return lists_of_dicts_data

    def add_user(self, new_user):
        """
        adds a new user to users
        :param new_user:
        :return all_users:
        """
        all_users = self.get_all_users()
        all_users.append(new_user)
        self.update_file(all_users)
        return all_users

    def update_file(self, list_of_dicts_file):
        """
        updates csv file
        :param list_of_dicts_file:
        :return None:
        """
        self.list_of_dicts_to_csv(list_of_dicts_file, self.filename)
