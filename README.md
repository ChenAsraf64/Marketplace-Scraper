# **marketplace-scraper**
_This is a web scraper developed to fetch product listings from different marketplaces given a specific search word. When operating on a product, it extracts its title, description, price, and image path. The scraper has been designed to be easily extensible to different marketplaces, starting with eBay._

## **Dependencies**

**scrapy**  
**pandas**  
**json**

## **Configuration and Extensibility**

### Marketplace Configuration

This scraper is powered by a configuration-driven approach. The configuration file, named `marketplace_configurations.py`, contains a dictionary (`search_url_dictionary`) structured as follows:

- **Key**: Name of the marketplace.
- **Value**: An array where each index has specific details:
    - **[0]**: URL template for search results. e.g., `'https://www.ebay.com/sch/i.html?...`
    - **[1]**: CSS selector for extracting individual item URLs.
    - **[2]**: CSS selector for extracting the next page URL.
    - **[3]**: URL template to fetch a specific item's description.
    - **[4]**: CSS selector for the item title.
    - **[5]**: CSS selector for the item price.
    - **[6]**: CSS selector for the primary image of the item.
    - **[7]**: CSS selector for the specific item number.

To illustrate, here's a sample configuration for eBay:

```python
search_url_dictionary = {
    'ebay' : [
        'https://www.ebay.com/sch/i.html?...', # Search result URL
        '.s-item__link::attr(href)', # Item URL
        '.pagination__next::attr(href)', # Next page URL
        'https://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?item={item_id}', # Item description
        'h1 span::text', # Item title
        '.x-price-primary span::text', # Item price
        '.ux-image-carousel-item img::attr(src)', # Primary image
        '.ux-layout-section__textual-display--itemId .ux-textspans--BOLD::text' # Item number
    ]
}
```
For integrating additional marketplaces, simply add the relevant configurations by adhering to the aforementioned structure. This approach ensures that the scraper is both extensible and maintainable.

## **Storage**
All scraped data is saved as JSON files in a dynamically created directory. Each product's properties are saved under the name: `[MARKETPLACE_NAME]_[PRODUCT_ID]`.json (For example, `Ebay_123456.json`). The folder's location corresponds to the running context of the scraper and is named according to the search word and the marketplace name. 


## **Note on User Agent**
The project's settings.py has been modified to utilize a specific USER_AGENT string tailored for eBay. Ensure to adjust this User-Agent or employ appropriate middlewares if targeting other websites or to evade potential scraping blocks.

## **Running Scraper**

1. `cd` to `marketplace_scraper` folder using shell.
2. Run the following command: `scrapy crawl marketplacespider -a marketplace_name={marketplace_name} -a search_word={search_word}`

Make sure to provide the appropriate values for {marketplace_name} and {search_word} when executing the command. If the search word contains more than one word, replace spaces with +. For example, "apple watch" should be "apple+watch".

**or**

1. Execute the main() function and provide the necessary inputs when prompted.