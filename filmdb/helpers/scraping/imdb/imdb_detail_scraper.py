import json
import logging
import re
import requests
from typing import Dict, Optional

from helpers import find_first


class ImdbDetailScraper:
    logger = logging.getLogger(__name__)

    def scrape(self, imdb_id: str) -> Optional[Dict]:
        response = requests.get(url=f"https://www.imdb.com/title/{imdb_id}/")
        response.raise_for_status()
        match = find_first(re.findall(r'<script type="application/ld\+json">(.*?)</script>', response.text))
        if not match:
            return None
        data = json.loads(match)
        if data['@type'] != 'Movie':
            return None
        try:
            return {
                'imdb_id': imdb_id,
                'title': data['name'],
                'year': find_first(data['datePublished'].split('-', 1)),
                'imdb_rating': data['aggregateRating']['ratingValue'],
                'imdb_votes': data['aggregateRating']['ratingCount'],
                'image': data['image']
            }
        except:
            self.logger.error(f"Error processing '{imdb_id}'")
            return None
