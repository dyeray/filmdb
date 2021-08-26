from typing import List, Dict, Tuple

import requests
from parsel import Selector

from helpers.scraping.cleaners import clean_title, extract_year

class LibibListScraper:

    def scrape(self, library_id: str, section: str, page: int) -> Tuple[List[Dict], bool]:
        # Request to list endpoint
        response = self._download(library_id, section, page)
        # Get json for list endpoint
        return self._extract(response)

    def _download(self, library_id: str, section: str, page: int) -> str:
        response = requests.post(
            url=f'https://{library_id}.libib.com/functions/items-list.php',
            data={
                "uri": section,
                "limit": f"{page * 36}",
                "letter_heading": "0",
                "group_heading": "",
                "letter": "all"
            },
            headers={
                'Referer': f'https://{library_id}.libib.com/i/{section}'
            }
        )
        response.raise_for_status()
        return response.text

    def _extract(self, html: str) -> Tuple[List[Dict], bool]:
        films = Selector(html).css('.cover')
        film_dicts = [self._extract_item(film) for film in films]
        return film_dicts, len(film_dicts) != 36

    def _extract_item(self, film: Selector):
        raw_title = film.css('.cover-title::text').get()
        return {
            'raw_title': raw_title,
            'title': clean_title(raw_title),
            'year': extract_year(raw_title),
            'id': film.css('::attr(id)').get().split('_')[1],
            'image_url': film.css('.cover_image::attr(src)').get()
        }


