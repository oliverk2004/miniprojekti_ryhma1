from scraper import Scraper


def main():
    scraper = Scraper()

    #Resolves to https://dl.acm.org/doi/10.1145/2380552.2380613
    title, authors, published = scraper.scrape("10.1145/2380552.2380613") 

    print(title)
    print(authors)
    print(published)
    print("end of scraping")



if __name__ == "__main__":
    main()