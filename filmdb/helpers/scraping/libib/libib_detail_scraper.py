from typing import Dict, Callable, Iterable

import requests
from parsel import Selector


class LibibDetailScraper:

    def scrape(self, library_id: str, section: str, copy_id: str) -> Dict:
        # Request to detail endpoint
        film_detail = self._download(library_id, section, copy_id)
        # Get json for detail endpoint
        return self._extract(film_detail)

    def _download(self, library_id: str, section: str, copy_id: str) -> str:
        response = requests.post(
            url=f'https://{library_id}.libib.com/functions/books-info-single.php',
            data={
                "join_id": copy_id,
            },
            headers={
                'Referer': f'https://{library_id}.libib.com/i/{section}'
            }
        )
        response.raise_for_status()
        return response.text

    def _extract(self, html: str) -> Dict:
        nodes = Selector(html).css('.book_data')
        pair_it = filter(lambda x: len(x) == 2, (''.join(node.css('::text').getall()).split(":") for node in nodes))
        film_data = {pair[0].strip(): pair[1].strip() for pair in pair_it}  # key values of .book_data
        return {
            'ean': film_data.get('EAN')
        }
