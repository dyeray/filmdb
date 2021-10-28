import requests
from fake_headers import Headers


class HttpClient:

    def __init__(self):
        self.headers = Headers()

    def get(self, url):
        return requests.get(url=url, headers=self.headers.generate())
