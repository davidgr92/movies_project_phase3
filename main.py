from storage.storage_json import StorageJson
from movie_app import MovieApp


def main():
    """Main function initialization"""
    storage_json_path = "storage/json_files/movies.json"
    storage = StorageJson(storage_json_path)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == '__main__':
    main()
