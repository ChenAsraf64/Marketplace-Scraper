from marketplace_scraper.spiders.marketplacespider import MarketplacespiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    #Get input from the user
    marketplace_name = input("Enter the marketplace name:")
    search_word = input("Enter the search word:")
    
    #Set up the CrawlerProcess with the project settings
    process = CrawlerProcess(get_project_settings())

    #Start the spider with the user inputs
    process.crawl(MarketplacespiderSpider, marketplace_name = marketplace_name, search_word = search_word)
    process.start()

if __name__ == "__main__":
    main()