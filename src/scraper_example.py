from scraper import Scraper


def main():
    scraper = Scraper()

    #Resolves to https://dl.acm.org/doi/10.1145/2380552.2380613
    lista = scraper.scrape("10.1145/2380552.2380613") 
    scraper.quit() 
    # You can use scrape method on multiple urls, but then always remember to quit after.
    # Otherwise you leave invisible browsers open and running.

    # The presentation is a work-in-progress.
    for row in lista:
        print(row)
    print("end of scraping")



if __name__ == "__main__":
    main()