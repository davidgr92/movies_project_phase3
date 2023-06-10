from os import environ
import requests
import pycountry


class MovieAPIRequest:
    """Movie API request class, gets movie from the API request
    and handles any errors."""
    def __init__(self):
        self.api_key = environ["API_KEY"]
        self.api_ep = f'http://www.omdbapi.com/?apikey={self.api_key}&t='

    def get_movie_data(self, title: str) -> dict:
        """Gets a movie title and tries to fetch movie data from api.
        Returns a dict of extracted data, if there is an error the function
        returns a dict with "error" as key and the error as it's value"""
        try:
            data = self.get_request_from_api(title)
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection error'}

        if 'Error' in data:
            return {'error': 'Movie not found!'}

        try:
            rating = float(data.get('imdbRating'))
        except ValueError:
            rating = data.get('imdbRating')

        else:
            return {data.get('Title').lower(): {
                'title': data.get('Title'),
                'rating': rating,
                'year': int(data.get('Year')),
                'genre': data.get('Genre'),
                'img': data.get('Poster'),
                'director': data.get('Director'),
                'country': data.get('Country'),
                'alpha_2': self.get_country_alpha_2(data.get('Country')),
                'imdbID': data.get('imdbID')
            }}

    def get_request_from_api(self, title: str):
        """Send a GET requests to API and returns response in json format"""
        url = self.api_ep + title
        response = requests.get(url, timeout=3)
        return response.json()

    @staticmethod
    def get_country_alpha_2(country_name: str) -> str:
        """Takes countries names from api response, and returns
        the 2-letter code of the first country
        """
        if ',' in country_name:
            countries_list = country_name.split(',')
            country_name = countries_list[0].strip()
        country = pycountry.countries.search_fuzzy(country_name)
        return country[0].alpha_2
