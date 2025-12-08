import requests
import time

class CrossrefAPI:
    BASE_URL = "https://api.crossref.org/works/"

    def __init__(self, http_get=requests.get, sleep=time.sleep):
        self.http_get = http_get
        self.sleep = sleep

    def fetch_doi(self, doi):
        url = f"{self.BASE_URL}{doi}"
        resp = self.http_get(url)
        self.sleep(1)

        if resp.status_code != 200:
            return None
        return resp.json()

class Scraper:
    """
    Web scraper class for getting reference data with a DOI tag.

    Methods:
        - scrape(str): Takes a DOI tag and returns the doi metadata.
    """
    def __init__(self, api=None):
        self.api = api or CrossrefAPI()

    def scrape(self, doi):
        data = self.api.fetch_doi(doi)
        if data is None:
            return None
        return [self.title(data), self.authors(data), self.published(data)]

    def title(self, data):
        return data["message"]["title"][0]

    def authors(self, data):
        author_names = ", ".join(
            f"{author.get('given', '')} {author.get('family', '')}".strip()
            for author in data["message"]["author"]
        )
        return author_names
    
    def published(self, data):
        return data["message"]["published"]["date-parts"][0][0]