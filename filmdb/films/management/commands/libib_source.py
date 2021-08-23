from django.core.management.base import BaseCommand

from films.models import Film, FilmCopy
from helpers.scraping.libib import LibibScraper
from typing import Dict, Iterable


class Command(BaseCommand):
    help = 'Imports films from Libib'

    def add_arguments(self, parser):
        parser.add_argument('library_id', type=str)
        parser.add_argument('--section', type=str, default='dvds')
        parser.add_argument('--skip_details', action='store_true')

    def handle(self, *args, **options):
        scraper = LibibScraper()
        library_id = options['library_id']
        section = options['section']
        skip_details = options['skip_details']
        page = 0
        last_page = False
        while not last_page:
            film_dicts, last_page = scraper.get_page(
                library_id=library_id,
                section=section,
                page=page,
                skip_details=skip_details
            )
            self.create_films(film_dicts, library_id)
            print(f"Scraped page {page}")
            page += 1

    def create_films(self, film_dicts: Iterable[Dict], location: str):
        # TODO: Commit once to database
        for film_dict in film_dicts:
            film = Film.objects.update_or_create(title=film_dict["title"])[0]
            FilmCopy.objects.update_or_create(
                location=location,
                copy_id=film_dict["id"],
                defaults={'film': film, 'ean': film_dict.get("ean")}
            )
