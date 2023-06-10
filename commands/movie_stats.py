class MovieStats:
    """Movies stats analyzer based on the provided movies data"""
    def __init__(self, movies_data):
        self.movies = movies_data
        self.ratings = self.get_ratings()
        self.average = self.average_rating(list(self.ratings.values()))
        self.median = self.median_rating(list(self.ratings.values()))
        self.best_movies = self.get_best_movies(self.ratings)
        self.worst_movies = self.get_worst_movies(self.ratings)

    def get_ratings(self):
        """Returns a dict with movie titles as keys
        and their rating as values"""
        return {val['title']: val['rating'] for val in self.movies.values()}

    def __str__(self):
        """Prints current statistics of provided movie data"""
        output = f"Average rating: {self.average:.2f}\n"
        output += f"Median rating: {self.median:.2f}\n"
        output += self.print_movies_list(self.best_movies)
        output += self.print_movies_list(self.worst_movies, best=False)
        return output

    @staticmethod
    def average_rating(ratings: list) -> float:
        """Takes a list of ratings and returns the average rating"""
        sum_ratings = 0
        for rating in ratings:
            sum_ratings += rating
        return sum_ratings / len(ratings)

    @staticmethod
    def median_rating(ratings: list) -> float:
        """Takes a list of ratings and returns the median rating"""
        ratings.sort()
        mid = len(ratings) // 2
        if len(ratings) % 2 == 0:
            return MovieStats.average_rating(ratings[mid - 1:mid + 1])
        return ratings[mid]

    @staticmethod
    def get_best_movies(movies_ratings: dict) -> list:
        """Takes a dict of movies names and ratings,
        returns all movies with the highest rating.
        """
        return [key for key, val in movies_ratings.items()
                if val == max(movies_ratings.values())]

    @staticmethod
    def get_worst_movies(movies_ratings: dict) -> list:
        """Takes a dict of movies names and ratings,
        returns all movies with the lowest rating.
        """
        return [key for key, val in movies_ratings.items()
                if val == min(movies_ratings.values())]

    @staticmethod
    def print_movies_list(movies_list: list, best: bool = True) -> str:
        """Prints all items in the provided enumerated list"""
        best_worst = "Worst"
        if best:
            best_worst = "Best"
        output_text = f"{best_worst} Movies: \n"
        for i, movie in enumerate(movies_list, 1):
            output_text += f'{i}. {movie}\n'
        return output_text
