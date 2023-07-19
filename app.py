"""
this module runs the movie web app
"""
from flask import Flask, render_template, redirect, request, url_for, flash
from moviweb_app.data_manager.json_data_manager import JSONDataManager
from moviweb_app.data_manager.csv_data_manager import CSVDataManager # when data is csv
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = "shalom"

data_manager = JSONDataManager("data/data.json")
# data_manager = CSVDataManager("data/data.csv")


@app.route('/')
def home():
    """
    route function to home page
    :return: index.html template
    """
    return render_template("index.html")


@app.route('/registration/<int:user_id>', methods=['GET', 'POST'])
def register(user_id):
    """
    route function to registration page
    :return: registration.html template
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data_manager.register(user_id, username, password)
        data_manager.login(user_id, username, password)
        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template("registration.html", user_id=user_id)


@app.route('/login/<int:user_id>', methods=['GET', 'POST'])
def login(user_id):
    """
    route function to registration page
    :return: login.html template
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data_manager.login(user_id, username, password)
        user = data_manager.get_user_by_id(user_id)
        if user["is_logged_in"]:
            return redirect(url_for('get_user_movies', user_id=user_id))
        flash("Wrong username/password!")
    return render_template("login.html", user_id=user_id)


@app.route('/users', methods=['GET'])
def list_users():
    """
    route function to /users page. gets all users data.
    :return: users.html template
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    """
    route function to a user page. gathers user's movies, name and id.
    :return: user_movies.html template
    """
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name_by_id(user_id)
    user = data_manager.get_user_by_id(user_id)
    if not user["is_logged_in"]:
        flash('You are not logged in!')
        return redirect(url_for('list_users'))

    if isinstance(user_movies, list) and user_name:
        return render_template('user_movies.html',
                               user_movies=user_movies,
                               user_name=user_name,
                               user_id=user_id,
                               )
    return render_template('404.html'), 404


@app.route('/users/add_user', methods=['GET', 'POST'])
def add_users():
    """
    route function to add a new user page.
    :return: user_movies.html template
    :return: users.html template
    """
    users = data_manager.get_all_users()

    if request.method == 'POST':
        name = request.form.get("name")

        new_user_id = data_manager.generate_user_id(users)
        new_user = data_manager.create_user_details(new_user_id, name)

        data_manager.add_user(new_user)

        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/delete_user', methods=['GET', 'DELETE'])
def delete_user(user_id):
    """
    route function to delete a user page.
    :return: users.html template
    """
    data_manager.delete_user(user_id)
    return redirect(url_for('list_users'))


@app.route('/users/<int:user_id>/update_user', methods=['GET', 'POST'])
def update_user(user_id):
    """
    route function to update a user page.
    if request is post:
    :return: user_movies.html template
    if request is get:
    :return: update_user.html template
    """
    if request.method == 'POST':
        new_name = request.form.get("name")
        data_manager.update_user(user_id, new_name)
        return redirect(url_for('get_user_movies', user_id=user_id))

    user = data_manager.get_user_by_id(user_id)
    return render_template('update_user.html', user_id=user_id, user=user)


def add_movie_details(form_objects_dict, user_id):
    """
    helper function to add a user's movie data (title, year, etc.).
    gathers data and returns a dictionary
    :return: new_movie
    """
    new_movie = data_manager.convert_form_data_to_new_movie_dict(form_objects_dict, user_id)
    api_data = data_manager.get_movies_api(new_movie["title"])
    new_movie_id = new_movie["movie_id"]
    if api_data and api_data['Response'] != 'False':
        new_movie = data_manager.get_api_data_to_dict(api_data, new_movie_id)
    return new_movie


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    route function to add a user's movie page.
    if request is post:
    :return: user_movies.html template
    if request is get:
    :return: add_movie.html template
    """
    if request.method == 'POST':
        form_objects_dict = request.form.to_dict()
        new_movie = add_movie_details(form_objects_dict, user_id)

        data_manager.add_movie(user_id, new_movie)

        return redirect(url_for('get_user_movies', user_id=user_id))

    return render_template('add_movie.html', user_id=user_id)


def get_updated_movie(form_dict, movie_id):
    """
    helper function to gather form data and return a movie dict
    :params: form_dict, movie_id
    :return: updated movie dict
    """
    title = form_dict.get("title")
    director = form_dict.get("director")
    year = form_dict.get("year")
    rating = form_dict.get("rating")
    updated_movie = {
        "movie_id": movie_id,
        "title": title,
        "director": director,
        "year": year,
        "rating": rating
    }
    return updated_movie


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST', 'PUT'])
def update_movie(user_id, movie_id):
    """
    route function to update a user's movie page.
    :params: user_id, movie_id
    if request is post:
    :return: user_movies.html template
    if request is get:
    :return: add_movie.html template
    """
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        updated_movie = get_updated_movie(form_dict, movie_id)
        data_manager.update_user_movie(user_id, movie_id, updated_movie)

        return redirect(url_for('get_user_movies', user_id=user_id))

    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    route function to delete a user's movie page.
    :params: user_id, movie_id
    :return: user_movies.html template
    """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    route function to "page not found" page.
    :params: user_id, movie_id
    :return: 404.html template
    """
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    route function to "internal server error" page.
    :params: user_id, movie_id
    :return: 500.html template
    """
    return render_template('500.html', error=error), 500


def reset_logging():
    """
    reset all users login to false every defined period of time
    :return:
    """
    data_manager.reset_logged_in()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p:"), "Logging has been reset..")


def set_reset_login(seconds):
    """sets seconds to reset user logging"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=reset_logging, trigger="interval", seconds=seconds)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    set_reset_login(seconds=15)
    app.run(debug=True)
