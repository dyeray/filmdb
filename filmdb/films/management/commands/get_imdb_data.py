import logging
from typing import Dict

from django.core.management.base import BaseCommand

from films.models import FilmCopy
from helpers.scraping.imdb import ImdbScraper


class Command(BaseCommand):
    help = 'Adds to the films additional info from IMDB'
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        films = FilmCopy.objects.filter(film__isnull=True)
        scraper = ImdbScraper()
        for film in films:
            film_dict = scraper.get_item(film.title, film.year)
            self.create_film(film_dict)

    def create_film(self, film_dicts: Dict):
        pass  # TODO: write film to database
