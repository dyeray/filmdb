import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from films.models import Film, FilmCopy
from helpers.scraping.libib import LibibScraper
from typing import Dict, Iterable


class Command(BaseCommand):
    help = 'Imports films from Libib'
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('library_id', type=str, help='Library to scrape')
        parser.add_argument('--section', type=str, default='dvds', help='Section of the website to scrape')
        parser.add_argument('--skip_details', action='store_true', help='Skips scraping the detail page')
        parser.add_argument('--first_page', type=int, default=1, help='First page to be scraped (1..n)')

    def handle(self, *args, **options):
        scraper = LibibScraper()
        library_id = options['library_id']
        page = options['first_page'] - 1
        last_page = False
        while not last_page:
            film_dicts, last_page = scraper.get_page(
                library_id=library_id,
                section=options['section'],
                page=page,
                skip_details=options['skip_details']
            )
            self.create_films(film_dicts, library_id)
            self.logger.info(f"Scraped page {page + 1}")
            page += 1

    @transaction.atomic
    def create_films(self, film_dicts: Iterable[Dict], location: str):
        for film_dict in film_dicts:
            FilmCopy.objects.update_or_create(
                location=location,
                copy_id=film_dict['id'],
                defaults={
                    'ean': film_dict.get('ean'),
                    'raw_title': film_dict['raw_title'],
                    'image_url': film_dict['image_url'],
                    'year': film_dict['year'],
                    'title': film_dict['title']
                }
            )
