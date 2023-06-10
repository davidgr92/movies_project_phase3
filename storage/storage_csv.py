import pandas as pd
from os.path import isfile
from .istorage import IStorage


class StorageCsv(IStorage):
    """CSV storage class, allows the movie app use csv format storage"""
    def __init__(self, file_path):
        self._file_path = file_path
        if not isfile(file_path):
            self.save_to_csv({})

    def save_to_csv(self, data):
        """Saves the provided data to a csv data file"""
        data_list = []
        headers = set()
        for key, value in data.items():
            headers.update(value.keys())
            data_list.append(value)

        df = pd.DataFrame(data_list, columns=list(headers))
        df.to_csv(self._file_path, index=False)

    def list_movies(self):
        """Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the storage
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
        df = pd.read_csv(self._file_path)
        movies_data = {}

        for i, row in df.iterrows():
            movie_dict = {}
            for key in df.columns:
                if pd.notna(row[key]):
                    movie_dict[key] = row[key]
            movies_data[row["title"].lower()] = movie_dict

        return movies_data

    def add_movie(self, movie_dict):
        """Adds a movie to the storage file.
        Loads the information from the storage file, add the movie,
        and saves it back to file. The function doesn't validate the input.
        """
        movies_data = self.list_movies()
        movies_data.update(movie_dict)
        self.save_to_csv(movies_data)

    def delete_movie(self, title):
        """Deletes a movie from the storage file.
        Loads the information from the storage file, deletes the movie,
        and saves it back to file. The function doesn't validate the input.
        """
        movies_data = self.list_movies()
        del movies_data[title]
        self.save_to_csv(movies_data)

    def update_movie(self, title, value, key="note"):
        """Updates a movie from the storage file.
        Loads the information from the storage file, updates the movie,
        and saves it back to file. The function doesn't validate the input.
        """
        movies_data = self.list_movies()
        movies_data[title][key] = value
        self.save_to_csv(movies_data)
