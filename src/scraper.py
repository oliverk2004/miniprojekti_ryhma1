from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import re

DOI_REGEX = re.compile(r"(10\.\d{1,50}/\S+)", re.IGNORECASE)

class Scraper:
    """
    Web scraper class for getting reference data with a DOI tag.

    Methods:
        - scrape(str): Takes a DOI tag and returns the data in a list.
        
        - quit(): Quits the webdriver, closing the invisible browser.
    """
    def __init__(self):
        # Initialize driver properly
        self.driver = self._init_driver()

    def _init_driver(self):
        # Use a proper Service object
        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # no visual browser, lighter and faster
        options.add_argument("--no-sandbox") # chrome security feature that might not work in CI and causes crash
        options.add_argument("--disable-dev-shm-usage") # tells chrome to not used shared memory. Temp files to disk instead to avoid issues where shm would be too small.
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        return webdriver.Chrome(service=service, options=options)
    
    def scrape(self, doi):
        osoite = self.resolve_url(doi)
        if osoite:
            self.driver.get(osoite)
            time.sleep(3)
            return self.extract_data()
        else:
            return []
    
    def extract_data(self):
        element_list = []
        title = self.driver.find_elements(By.CSS_SELECTOR, 'h1[property="name"]')
        authors = self.driver.find_elements(By.CLASS_NAME, "authors")
        published = self.driver.find_elements(By.CLASS_NAME, 'core-published')

        element_list.append([
            title[0].text,
            authors[0].text,
            published[0].text
        ])

        return element_list
    
    def is_valid_doi(self,doi):
        return bool(DOI_REGEX.match(doi))
    
    def quit(self):
        self.driver.quit()

    def resolve_url(self, doi):
        if self.is_valid_doi(doi):
            osoite = f'https://doi.org/{doi}'
            response = requests.get(osoite, allow_redirects=True)

            if response.history:
                # Request was redirected, meaning the doi tag leads to something.
                return response.url
            else:
                print("DOI not found")
                return ""
