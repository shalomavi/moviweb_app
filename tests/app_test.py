"""
tests module
"""
import json
from moviweb_app.app import delete_movie, add_movie, update_movie, delete_user, add_users
from moviweb_app.data_manager.json_data_manager import JSONDataManager
import pytest

users = [
    {
        "user_id": 1,
        "name": "name",
        "movies":
            [
                {
                    "movie_id": 1,
                    "title": "title",
                    "director": "director",
                    "year": 1988,
                    "rating": 8.8,
                    "poster": "poster",
                    "address": "address"
                }
            ]
    }

]

new_movie = {
    "movie_id": 2,
    "title": "title",
    "director": "director",
    "year": 1988,
    "rating": 8.8,
    "poster": "poster",
    "address": "address"
}

updated_movie = {
    "movie_id": 1,
    "title": "updated_title",
    "director": "director",
    "year": 1988,
    "rating": 8.8,
    "poster": "poster",
    "address": "address"
}

new_user = {
    "user_id": 2,
    "name": "name_2",
    "movies":
        [
            {
                "movie_id": 1,
                "title": "title",
                "director": "director",
                "year": 1988,
                "rating": 8.8,
                "poster": "poster",
                "address": "address"
            }
        ]
}
updated_user = {
    "user_id": 1,
    "name": "name_2",
    "movies":
        [
            {
                "movie_id": 1,
                "title": "title",
                "director": "director",
                "year": 1988,
                "rating": 8.8,
                "poster": "poster",
                "address": "address"
            }
        ]
}

def refresh_file():
    with open("test_file.json", "w") as f:
        f.write(json.dumps(users, indent=4))


def load_file():
    with open("test_file.json", "r") as f:
        data = json.loads(f.read())
    return data


refresh_file()
dm = JSONDataManager("test_file.json")


def test_delete_movie_dm():
    dm.delete_movie(1, 1)
    data = load_file()
    assert len(data[0]["movies"]) == 0
    refresh_file()


def test_delete_movie_wrong_movie_id_dm():
    dm.delete_movie(1, 2)
    data = load_file()
    assert len(data[0]["movies"]) == 1
    refresh_file()


def test_delete_movie_wrong_user_id_dm():
    dm.delete_movie(2, 1)
    data = load_file()
    assert len(data[0]["movies"]) == 1
    refresh_file()


def test_add_movie_dm():
    dm.add_movie(1, new_movie)
    data = load_file()
    assert len(data[0]["movies"]) == 2
    refresh_file()


def test_add_movie_dm_empty():
    dm.add_movie(1, None)
    data = load_file()
    assert len(data[0]["movies"]) == 2
    refresh_file()


def test_update_movie_dm():
    dm.update_user_movie(1, 1, updated_movie)
    assert dm.get_movie_by_id(1, 1) == updated_movie
    refresh_file()


def test_update_movie_dm_wrong_id():
    dm.update_user_movie(1, 2, updated_movie)
    assert dm.get_movie_by_id(1, 1) != updated_movie
    refresh_file()


def test_get_movie_by_id_dm():
    data = load_file()
    assert dm.get_movie_by_id(1, 1) == data[0]["movies"][0]
    refresh_file()


def test_get_movie_by_id_dm_wrong_id():
    data = load_file()
    assert dm.get_movie_by_id(1, 2) != data[0]["movies"][0]
    refresh_file()


def test_add_user_dm():
    dm.add_user(new_user)
    data = load_file()
    assert len(data) == 2
    refresh_file()


def test_delete_user_dm():
    dm.delete_user(1)
    data = load_file()
    assert len(data) == 0
    refresh_file()


def test_delete_user_dm_wrong_id():
    dm.delete_user(2)
    data = load_file()
    assert len(data) == 1
    refresh_file()


def test_update_user_dm():
    dm.update_user_movie(1, 1, new_user)
    data = load_file()
    assert data[0] != users[0]
    refresh_file()


def test_update_user_dm_wrong_id():
    dm.update_user_movie(2, 1, new_user)
    data = load_file()
    assert data[0] == users[0]
    refresh_file()

# Todo: complete all tests on app.py file..
def test_delete_movie():
    # delete_movie(1, 1)
    # assert len(users[0]["movies"]) == 0
    # refresh_file()
    pass


def test_update_movie():
    pass
    refresh_file()


def test_read_movie():
    pass
    refresh_file()


def test_add_user():
    pass
    refresh_file()


def test_delete_user():
    pass
    refresh_file()


def test_update_user():
    pass
    refresh_file()


def test_add_users():
    pass
    refresh_file()


pytest.main()
