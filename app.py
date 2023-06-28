from flask import Flask, render_template, redirect, request, url_for

from data_manager.json_data_manager import JSONDataManager


app = Flask(__name__)
data_manager = JSONDataManager("data/data.json")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name_by_id(user_id)
    return render_template('user_movies.html',
                           user_movies=user_movies,
                           user_name=user_name, user_id=user_id)


@app.route('/users/add_user', methods=['GET', 'POST'])
def add_users():
    users = data_manager.get_all_users()

    if request.method == 'POST':
        name = request.form.get("name")
        title = request.form.get("title")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = request.form.get("rating")
        new_user_id = generate_user_id(users)
        movie_id = generate_movie_id(new_user_id)
        new_movie = {
            "id": movie_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating
        }
        new_user = {
            "id": new_user_id,
            "name": name,
            "movies": [new_movie]
        }
        print("id", new_user_id)
        print(new_user)
        print(data_manager.add_user(new_user))

        return redirect(url_for('home'))

    return render_template('add_user.html')


def generate_user_id(users):
    if not users:
        return 1
    return max([user["id"] for user in users]) + 1


def generate_movie_id(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    if not user_movies:
        return 1
    return max([movie["id"] for movie in user_movies]) + 1


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form.get("title")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = request.form.get("rating")
        new_id = generate_movie_id(user_id)
        new_movie = {
            "id": new_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating
        }
        data_manager.add_movie(user_id, new_movie)

        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        title = request.form.get("title")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = request.form.get("rating")
        updated_movie = {
            "id": movie_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating
        }
        data_manager.update_user_movie(user_id, movie_id, updated_movie)

        return redirect(url_for('get_user_movies', user_id=user_id))

    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


def main():
    jdata = JSONDataManager("data/data.json")
    print(jdata.get_all_users())
    print(jdata.get_user_movies(1))
    updated_movie = {
        "id": 1,
        "name": "Inception",
        "director": "Christopher Nolan",
        "year": 2010,
        "rating": 8.8
    }
    print(jdata.update_user_movie(1, 1, updated_movie))
    print(jdata.get_user_movies(1))


if __name__ == "__main__":
    # main()
    app.run(debug=True)
