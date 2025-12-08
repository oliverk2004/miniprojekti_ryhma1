from src.scraper import Scraper
import unittest

class MockAPI:
    def fetch_doi(self, doi):
        return {
            'message': {
                'title': ['Aku Ankan Tarinat vol. 1'],
                'author': [
                    {'given': 'Aku', 'family': 'Ankka'},
                    {'given': 'Roope', 'family': 'Ankka'}
                ],
                'published': {'date-parts': [[2021,10,11]]}
            }
        }
    
class TestScraper(unittest.TestCase):

    def setUp(self):
        self.api = MockAPI()
        self.scraper = Scraper(api=self.api)

    def test_scrape(self):
        data = self.scraper.scrape("10.1145/2380552.2380613")
        self.assertEqual(data[0], "Aku Ankan Tarinat vol. 1")
        self.assertEqual(data[1], "Aku Ankka, Roope Ankka")
        self.assertEqual(data[2], 2021)
