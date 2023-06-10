import pytest
import os
from pathlib import Path
from se105_3.movies_project.storage.storage_json import StorageJson
from se105_3.movies_project.storage.istorage import IStorage
from se105_3.movies_project.storage.storage_csv import StorageCsv

ROOT_PATH = Path(__file__).parent.parent
DATA = {"forrest gump": {
            "title": "Forrest Gump",
            "rating": 8.8,
            "year": 1994,
            "genre": "Drama, Romance",
            "img": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
            "director": "Robert Zemeckis",
            "country": "United States",
            "alpha_2": "US",
            "imdbID": "tt0109830"}}
DATA2 = {"the lion king": {
            "title": "The Lion King",
            "rating": 8.5,
            "year": 1994,
            "genre": "Animation, Adventure, Drama",
            "img": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_SX300.jpg",
            "director": "Roger Allers, Rob Minkoff",
            "country": "United States",
            "alpha_2": "US",
            "imdbID": "tt0110357"}}


def test_storage_json_init():
    path = os.path.join(ROOT_PATH, "storage", "json_files", "movies.json")
    storage = StorageJson(path)
    assert isinstance(storage, IStorage)
    assert isinstance(storage, StorageJson)


def test_storage_json_list_movies():
    path = os.path.join(ROOT_PATH, "storage", "json_files", "david.json")
    storage = StorageJson(path)
    storage.save_to_json(DATA)
    assert storage.list_movies() == DATA
    assert len(storage.list_movies()) == 1


def test_storage_json_add_movie():
    path = os.path.join(ROOT_PATH, "storage", "json_files", "david.json")
    storage = StorageJson(path)
    storage.add_movie(DATA2)
    assert len(storage.list_movies()) == 2


def test_storage_json_del_movie():
    path = os.path.join(ROOT_PATH, "storage", "json_files", "david.json")
    storage = StorageJson(path)
    movie_title = list(DATA.keys())[0]
    storage.delete_movie(movie_title)
    assert storage.list_movies() == DATA2
    assert len(storage.list_movies()) == 1


def test_storage_json_update_movie():
    path = os.path.join(ROOT_PATH, "storage", "json_files", "david.json")
    storage = StorageJson(path)
    movie_title = list(DATA2.keys())[0]
    note = "Bla bla"
    storage.update_movie(movie_title, note)
    assert storage.list_movies()[movie_title]["note"] == note


def test_storage_csv_init():
    path = os.path.join(ROOT_PATH, "storage", "csv_files", "david.json")
    storage = StorageCsv(path)
    assert isinstance(storage, IStorage)
    assert isinstance(storage, StorageCsv)


def test_storage_csv_list_movies():
    pass


def test_storage_csv_add_movie():
    pass


def test_storage_csv_del_movie():
    pass


def test_storage_csv_update_movie():
    pass


pytest.main()
