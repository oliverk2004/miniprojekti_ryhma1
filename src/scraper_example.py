from scraper import Scraper


def main():
    scraper = Scraper()

    #Resolves to https://dl.acm.org/doi/10.1145/2380552.2380613
    data = scraper.scrape("10.1145/2380552.2380613")

    if data is None:
        print("DOI virheellinen")
    else:
        print(data[0])
        print(data[1])
        print(data[2])

if __name__ == "__main__":
    main()
