from typing import Optional, Dict

from helpers.scraping.imdb.imdb_detail_scraper import ImdbDetailScraper
from helpers.scraping.imdb.imdb_search_scraper import ImdbSearchScraper


class ImdbScraper:

    def __init__(self):
        self.search_scraper = ImdbSearchScraper()
        self.detail_scraper = ImdbDetailScraper()

    def get_item(self, title: str, year: Optional[int]) -> Optional[Dict]:
        url = self.search_scraper.scrape(title, year)
        if not url:
            return None
        return self.detail_scraper.scrape(url)
