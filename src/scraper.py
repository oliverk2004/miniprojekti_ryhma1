import requests
import time

class Scraper:
    """
    Web scraper class for getting reference data with a DOI tag.

    Methods:
        - scrape(str): Takes a DOI tag and returns the doi metadata.
    """
    def __init__(self):
        # Initialize driver properly
        # self.driver = self._init_driver()
        pass

    def scrape(self, doi):
        osoite = f"https://api.crossref.org/works/{doi}"
        response = requests.get(osoite)
        time.sleep(1)
        data = response.json()
        return self.title(data), self.authors(data), self.published(data)

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