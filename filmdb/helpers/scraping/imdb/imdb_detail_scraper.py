import html
import json
import logging
import re
from typing import Dict, Optional

from helpers import find_first
from helpers.scraping.http_client import HttpClient


class ImdbDetailScraper:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.client = HttpClient()

    def scrape(self, imdb_id: str) -> Optional[Dict]:
        response = self.client.get(url=f"https://www.imdb.com/title/{imdb_id}/")
        response.raise_for_status()
        match = find_first(re.findall(r'<script type="application/ld\+json">(.*?)</script>', response.text))
        if not match:
            return None
        data = json.loads(match)
        title = html.unescape(data['name'])
        if data['@type'] != 'Movie':
            return None
        try:
            year = self.get_year(data, response.text)
            if not year:
                return None
            return {
                'imdb_id': imdb_id,
                'title': title,
                'year': year,
                'imdb_rating': data['aggregateRating']['ratingValue'] if 'aggregateRating' in data else None,
                'imdb_votes': data['aggregateRating']['ratingCount'] if 'aggregateRating' in data else 0,
                'image': data.get('image', None)
            }
        except:
            self.logger.error(f"Error processing '{imdb_id}'")
            return None

    def get_year(self, data, text) -> Optional[int]:
        publish_date = data.get('datePublished', None)
        json_date = find_first(publish_date.split('-', 1) if publish_date else [])
        if json_date:
            return int(json_date)
        regex_year = find_first(re.findall(r'"releaseYear":{"year":(\d+),', text))
        return int(regex_year) if regex_year else None
