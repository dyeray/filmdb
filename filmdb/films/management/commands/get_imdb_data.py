import logging
from typing import Dict, Optional

from django.core.management.base import BaseCommand
from django.db import transaction

from films.models import FilmCopy, Film
from helpers.scraping.imdb import ImdbScraper


class Command(BaseCommand):
    help = 'Adds to the films additional info from IMDB'
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        copies = FilmCopy.objects.filter(film__isnull=True)
        scraper = ImdbScraper()
        for film_copy in copies:
            film_dict = scraper.get_item(film_copy.title, film_copy.year)
            self.create_film(film_dict, film_copy)

    @transaction.atomic
    def create_film(self, film_dict: Optional[Dict], copy: FilmCopy):
        if film_dict:
            self.logger.info(f"Adding '{film_dict['title']}'")
            film, _ = Film.objects.update_or_create(
                imdb_id=film_dict['imdb_id'],
                defaults={
                    'title': film_dict['title'],
                    'year': film_dict['year'],
                    'imdb_rating': film_dict['imdb_rating'],
                    'imdb_votes': film_dict['imdb_votes'],
                    'image_url': film_dict['image']
                }
            )
            copy.refresh_from_db()
            copy.film = film
            copy.save()
        else:
            self.logger.info(f"Skipping item '{copy.title}'")
            film, _ = Film.objects.get_or_create(imdb_id="dummy", defaults={
                'title': "dummy",
                'year': 2000,
                'imdb_rating': None,
                'imdb_votes': 0,
                'image_url': None
            })
            copy.refresh_from_db()
            copy.film = film
            copy.save()
            return
