import random
from thefuzz import process
import matplotlib.pyplot as plt
from commands.api_request import MovieAPIRequest
from commands.movie_stats import MovieStats
from commands.web_gen import WebGenerator


class MovieApp:
    """Movie application main class"""
    def __init__(self, storage):
        self.storage = storage
        self.func_dict = {
            0: self.exit_program,
            1: self.list_movies,
            2: self.add_movie,
            3: self.delete_movie,
            4: self.update_movie,
            5: self.stats,
            6: self.random_movie,
            7: self.search_movie,
            8: self.sort_movies,
            9: self.generate_histogram,
            10: self.generate_website
        }

    def run(self):
        """Function to run the movie app"""
        print("********** My Movies Database **********")

        try:
            action = self.choose_action()
            while action:
                self.func_dict[action]()
                self.post_action_buffer()
                action = self.choose_action()
        except self.BreakException:
            pass

    def print_menu(self) -> None:
        """Prints menu each command name and number in a new line
        from the functions dictionary"""
        print('Menu:')
        for key, val in self.func_dict.items():
            func_name = val.__name__.replace('_', ' ')
            print(f'{key}. {func_name.title()}')

    @staticmethod
    def post_action_buffer() -> None:
        """Creates a one line buffer in CLI and awaits for user keyboard click"""
        input("\nPress enter to continue\n")

    def choose_action(self) -> int:
        """Asks user to choose an action by num, check that it's a valid input
        and return a valid int input number
        """
        self.print_menu()
        action = input("Enter choice (0-10): ")
        while self.validate_action(action):
            print("Invalid choice")
            action = input("Enter choice (0-10): ")
        print()
        return int(action)

    def validate_action(self, user_input) -> bool:
        """Validates user input, first that it's numeric, and then that
        key exists in functions dict, Returns bool var accordingly.
        """
        if user_input.isnumeric() and int(user_input) in self.func_dict:
            return False
        return True

    # ======================== Action 0. Quit program ==========================
    def exit_program(self) -> None:
        """Raises an exception to break out of the main loop"""
        raise self.BreakException

    class BreakException(BaseException):
        """Exception to break out of main loop"""

    # ======================= Action 1. List all movies ========================
    def list_movies(self, movie_data=None) -> None:
        """Gets movies data from json file or by parameter and prints it
        line by line with rating and release year.
        """
        if movie_data is None:
            movies = self.storage.list_movies()
        else:
            movies = movie_data

        for info in movies.values():
            print(f'{info["title"]}: {info["rating"]:.1f}/10 ({info["year"]})')
        print(f'{len(movies)} movies in total\n')

    # ========================== Action 2. Add movie ===========================
    def add_movie(self, title=None) -> None:
        """Adds a movie by fetching data from api, if title is not provided asks
        user then saves new entry to the json data file.
        """
        movies = self.storage.list_movies()
        movie_name = self.get_title(title, operation='add')

        if movie_name in movies:
            print(f"Movie '{movies[movie_name]['title']}' already exists")
        else:
            movie_api_request = MovieAPIRequest()
            new_movie_dict = movie_api_request.get_movie_data(movie_name)
            if new_movie_dict.get('error'):
                # If error in fetching data, output the error message.
                print(new_movie_dict['error'])
            else:
                self.storage.add_movie(new_movie_dict)
                print(f"Movie '{new_movie_dict[movie_name]['title']}' "
                      f"successfully added")

    # ================ Assisting function for commands 2, 3, 4 ================
    @staticmethod
    def get_title(title, operation: str) -> str:
        """If title is provided returns it, otherwise asks user for input"""
        if title is None:
            return input(f"Enter movie name to {operation}: ").lower()
        return title.lower()

    # ========================= Action 3. Delete movie =========================
    def delete_movie(self, title=None) -> None:
        """Deletes a movie entry from json file. If title is not provided
        prompts the user to input title to delete.
        """
        movies = self.storage.list_movies()
        movie_name = self.get_title(title, operation='delete')

        if movie_name in movies:
            self.storage.delete_movie(movie_name)
            print(f"Movie '{movies[movie_name]['title']}' successfully deleted")
        else:
            print(f"Movie '{movie_name}' doesn't exist!")

    # ==================== Action 4. Update movie (Add note) ===================
    def update_movie(self, title=None, note=None) -> None:
        """Updates a movie entry with a personal note. If either title or note
        are not provided, prompts the user for input.
        """
        movies = self.storage.list_movies()
        movie_name = self.get_title(title, operation='update')

        if movie_name in movies:
            if note is None:
                note_input = input("Enter a note to add to the movie: ")
            else:
                note_input = note
            self.storage.update_movie(movie_name, note_input)
            print(f"Movie '{movies[movie_name]['title']}' successfully updated")
        else:
            print(f"Movie '{movie_name}' doesn't exist!")

    # ========================== Action 5. Statistics ==========================
    def stats(self) -> None:
        """Prints statistics of current data from the json file,
        average movie rating, median movie rating,
        and movie/s with best and worst ratings"""
        movies = self.storage.list_movies()
        print(MovieStats(movies))

    # ========================= Action 6. Random movie =========================
    def random_movie(self) -> None:
        """Prints random movie from the json data"""
        movies = self.storage.list_movies()
        info = random.choice(list(movies.values()))
        print(f"Your movie for tonight: {info['title']} ({info['year']}), "
              f"it's rated {info['rating']}/10")

    # ========================= Action 7. Search movie =========================
    def search_movie(self) -> None:
        """Asks user for the search query, then searches for exact match,
        if not found search for approximate match and prints the results
        """
        search_accuracy = 75

        movies = self.storage.list_movies()
        search_query = input("Enter part of the movie name: ")

        search_results = [movie_name for movie_name in movies
                          if search_query.lower() in movie_name]

        # If no results found during exact search, checks for fuzzy search
        if not search_results:
            print(f"The exact search '{search_query}' didn't yield results.")
            search_results = [mov_name for mov_name, ratio in process.extract(
                search_query, list(movies.keys())) if ratio > search_accuracy]
            if search_results:
                print("Maybe you meant:")

        # If found matches in search, print them line by line
        if search_results:
            for title in search_results:
                print(f"{movies[title]['title']}: {movies[title]['rating']}/10 "
                      f"({movies[title]['year']})")
        else:
            print("No results found in Fuzzy search as-well.")

    # ==================== Action 8. Sort and print movies =====================
    def sort_movies(self, is_descending=True) -> None:
        """Print movies in a sorted order, by default in descending
        order by rating.
        """
        movies = self.storage.list_movies()
        sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'],
                             reverse=is_descending)
        sorted_dict = {key[0]: key[1] for key in sorted_list}
        self.list_movies(movie_data=sorted_dict)

    # ======================= Action 9. Save histogram =========================
    def generate_histogram(self, file_name: str = 'histogram') -> None:
        """Generate histogram image from movies ratings in json file"""
        movies = self.storage.list_movies()
        ratings = [val['rating'] for key, val in movies.items()]
        plt.hist(ratings, bins=range(10))
        plt.xlabel('Ratings')
        plt.ylabel('Amount of Movies')
        plt.savefig(f'{file_name}.png')
        print(f"Rating histogram '{file_name}.png' is ready.")

    # ===================== Action 10. Generate a website ======================
    def generate_website(self) -> None:
        """Generate a html file from the index template, serialize data from
        json file and embed serialized data in the new html file
        """
        movies = self.storage.list_movies()
        generator = WebGenerator(movies)
        generator.generate_web_page()
        print("Website was successfully generated.")
