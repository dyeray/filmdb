from typing import Dict
import requests

class ImdbDetailScraper:
    def scrape(self, imdb_id: str) -> Dict:
        response = requests.get(url=f"https://www.imdb.com/title/{imdb_id}/")
        response.raise_for_status()
        return {}  # TODO: Scrape detail page
