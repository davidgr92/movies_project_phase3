import json
from os.path import isfile
from .istorage import IStorage


class StorageJson(IStorage):
    """Json storage class, allows the movie app use json format storage"""
    def __init__(self, file_path):
        self._file_path = file_path
        if not isfile(file_path):
            self.save_to_json({})

    def save_to_json(self, data):
        """Saves the provided data to the json data file"""
        with open(self._file_path, 'w') as file:
            file.write(json.dumps(data, indent=4))

    def list_movies(self):
        """Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the JSON
        file and returns the data.

        For example, the function may return:
        {
          "titanic": {
            "title": "Titanic",
            "rating": 9,
            "year": 1999
            ...
          },
          "..." {
            ...
          },
        }
        """
        with open(self._file_path, 'r') as file:
            movie_data = json.loads(file.read())

        return movie_data

    def add_movie(self, movie_dict):
        """Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies_data = self.list_movies()
        movies_data.update(movie_dict)
        self.save_to_json(movies_data)

    def delete_movie(self, title):
        """Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies_data = self.list_movies()
        del movies_data[title]
        self.save_to_json(movies_data)

    def update_movie(self, title, value, key="note"):
        """Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies_data = self.list_movies()
        movies_data[title][key] = value
        self.save_to_json(movies_data)
