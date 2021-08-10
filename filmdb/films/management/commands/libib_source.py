import requests
from parsel import Selector

from django.core.management.base import BaseCommand

from films.models import Film, FilmCopy


class Command(BaseCommand):
    help = 'Imports films from Libib'

    def add_arguments(self, parser):
        parser.add_argument('library_id', type=str)
        parser.add_argument('--section', type=str, default='dvds')

    def handle(self, *args, **options):
        library_id = options["library_id"]
        section = options['section']
        response = requests.post(
            url=f'https://{library_id}.libib.com/functions/items-list.php',
            data={
                "uri": section,
                "limit": "0",
                "letter_heading": "0",
                "group_heading": "",
                "letter": "all"
            },
            headers={
                'Referer': f'https://{library_id}.libib.com/i/{section}'
            }
        )
        response.raise_for_status()
        selector = Selector(response.text)
        films = selector.css('.cover')
        film_dicts = [self.extract_data(film) for film in films]
        self.create_films(film_dicts, library_id)

    def extract_data(self, film: Selector):
        return {
            'title': film.css('.cover-title::text').get(),
            'id': film.css('::attr(id)').get().split('_')[1]
        }

    def create_films(self, film_dicts: list[dict], location: str):
        for film_dict in film_dicts:
            film = Film.objects.create(title=film_dict["title"])
            FilmCopy.objects.create(location=location, copy_id=film_dict["id"], film=film, ean="")
