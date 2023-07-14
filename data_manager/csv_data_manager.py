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
            writer.writerow(['user_id', 'name',
                             'movie_id', 'title',
                             'director', 'year',
                             'rating', 'poster',
                             'address'])
            # Write the data rows
            for item in data:
                user_id = item['user_id']
                name = item['name']
                movies = item['movies']
                for movie in movies:
                    movie_id = movie.get('movie_id', 00)
                    title = movie.get('title', "ADD Movies as you wish")
                    director = movie.get('director')
                    year = movie.get('year')
                    rating = movie.get('rating')
                    poster = movie.get('poster')
                    address = movie.get('address')
                    writer.writerow([user_id, name, movie_id,
                                     title, director, year,
                                     rating, poster, address])

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
            user_dict = {
                "user_id": int(user[0]),
                "name": user[1],
                "movies": []
            }
            if user[2]:
                movie = {
                    "movie_id": int(user[2]),
                    "title": user[3],
                    "director": user[4],
                    "year": int(user[5]) if type(user[5]) == int else user[5],
                    "rating": float(user[6]) if type(user[6]) == float else user[6],
                    "poster": user[7],
                    "address": user[8],
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
