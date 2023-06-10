import os
from pathlib import Path


class WebGenerator:
    """Website generator class - allows to create movies website"""
    main_project_dir = Path(__file__).parent.parent
    template_path = os.path.join(main_project_dir,
                                 "_static", "index_template.html")
    new_index_path = os.path.join(main_project_dir,
                                  "_static", "index.html")

    def __init__(self, movies_data, new_path=new_index_path):
        self.movies = movies_data
        self.new_path = new_path

    def generate_web_page(self) -> None:
        """Generate a html file from the index template, serialize data from
        json file and embed serialized data in the new html file
        """
        template = self.get_html_template(WebGenerator.template_path)
        serialized_data = self.serialize_all_data()
        self.create_html_file(self.new_path, template, serialized_data)

    def create_html_file(self, new_path, template, serialized_data):
        """Create or recreate the html file in the new path, based on provided template
        and replace placeholders with serialized data"""
        with open(new_path, 'w') as file:
            new_html = self.replace_template_placeholders(template,
                                                          serialized_data)
            file.write(new_html)

    @staticmethod
    def replace_template_placeholders(template, serialized_data):
        """Replaces the placeholders in the template"""
        new_html = template.replace('        __TEMPLATE_MOVIE_GRID__',
                                    serialized_data)
        return new_html.replace('__TEMPLATE_TITLE__', 'David\'s Movies List')

    def serialize_all_data(self) -> str:
        """Reads data from json file and generates a html serialized version
        from data. Returns a html string with all items from the json data file.
        """
        serialized_data = ''
        for movie_info in self.movies.values():
            serialized_data += self.serialize_single_data_item(movie_info)
        return serialized_data

    @staticmethod
    def serialize_single_data_item(movie_dict: dict) -> str:
        """Gets single movie dict, generate serialized html element
        and returns the html string.
        """
        output_html = f'''\t\t<li><div class="movie tooltip">
    \t\t\t<a href="https://www.imdb.com/title/{movie_dict["imdbID"]}/" target="_blank">
    \t\t\t<div class="ribbon-wrapper"><div class="ribbon">{movie_dict["rating"]}/10</div></div>
    \t\t\t<img class="movie-poster" src="{movie_dict["img"]}"></a>
    \t\t\t<div class="movie-info">
    \t\t\t\t<div class="movie-text">
    \t\t\t\t\t<div class="movie-title">{movie_dict["title"]}</div>
    \t\t\t\t\t<div class="movie-year">{movie_dict["year"]}</div>
    \t\t\t\t</div>
    \t\t\t\t<img class="country"src="https://flagsapi.com/{movie_dict["alpha_2"]}/flat/64.png"></div>
    '''
        if movie_dict.get('note'):
            output_html += f'\t\t\t\t<span class="tooltiptext">{movie_dict["note"]}</span>'
        output_html += '\t\t\t</div>\n'
        return output_html

    @staticmethod
    def get_html_template(path: str) -> str:
        """Returns a copy of provided path file as string data"""
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
