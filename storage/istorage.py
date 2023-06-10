from abc import ABC, abstractmethod


class IStorage(ABC):
    """Persistent storage management abstract class"""
    @abstractmethod
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

    @abstractmethod
    def add_movie(self, movie_dict):
        """Adds a movie to the storage file.
        Loads the information from the storage file, add the movie,
        and saves it back to file. The function doesn't validate the input.
        """

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the storage file.
        Loads the information from the storage file, deletes the movie,
        and saves it back to file. The function doesn't validate the input.
        """

    @abstractmethod
    def update_movie(self, title, value, key="note"):
        """Updates a movie from the storage file.
        Loads the information from the storage file, updates the movie,
        and saves it back to file. The function doesn't validate the input.
        """
