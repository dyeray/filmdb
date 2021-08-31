from typing import Optional
from helpers import find_first
from helpers.scraping import parsel_utils
import re

import requests
from parsel import Selector


class ImdbSearchScraper:
    regex = r"/title/(.+)/"

    def scrape(self, title: str, year: Optional[int]) -> Optional[str]:
        response = requests.get(
            url=f'https://www.imdb.com/find?q={title}',
        )
        response.raise_for_status()
        selector = Selector(response.text)
        film_nodes = selector.xpath(
            "//*[@class='findList'][ancestor::*[@class='findSection'][descendant::a[@name='tt']]]"
            "//*[contains(@class, 'findResult')]"
        )
        film_node = None
        if year is None:
            film_node = find_first(film_nodes)
        else:
            film_dist = 2
            for node in film_nodes:
                node_text = parsel_utils.get_node_text(node.css('.result_text'))
                scraped_year = int(find_first(re.findall(r"\((\d+)\)", node_text)))
                dist = abs(scraped_year - year)
                if dist < film_dist:
                    film_dist = dist
                    film_node = node
        if not film_node:
            return None
        return find_first(re.findall(self.regex, film_node.css('.result_text a::attr(href)').get()))

