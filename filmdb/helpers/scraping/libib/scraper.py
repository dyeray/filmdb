from typing import List, Dict, Tuple

from .libib_detail_scraper import LibibDetailScraper
from .libib_list_scraper import LibibListScraper


class LibibScraper:

    def __init__(self):
        self.list_scraper = LibibListScraper()
        self.detail_scraper = LibibDetailScraper()

    def get_page(self, library_id: str, section: str, page: int, skip_details: bool) -> Tuple[List[Dict], bool]:
        films, last_page = self.list_scraper.scrape(library_id, section, page)
        if not skip_details:
            films = [{**film, **self.detail_scraper.scrape(library_id, section, film['id'])} for film in films]
        return films, last_page
