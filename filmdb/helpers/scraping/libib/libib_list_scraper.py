from typing import List, Dict, Tuple

import requests
from parsel import Selector


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
        film_dicts = [{
            'title': film.css('.cover-title::text').get(),
            'id': film.css('::attr(id)').get().split('_')[1]
        } for film in films]
        return film_dicts, len(film_dicts) != 36
