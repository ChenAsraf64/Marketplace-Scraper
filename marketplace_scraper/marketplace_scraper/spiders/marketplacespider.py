import scrapy
import requests
import json
import os
from marketplace_configurations import search_url_dictionary


class MarketplacespiderSpider(scrapy.Spider):
    name = "marketplacespider"
    
    def __init__(self, marketplace_name = None, search_word = None):
        super(MarketplacespiderSpider, self).__init__()

        # If the marketplace exists in the dictionary, extract marketplace search word URL
        if marketplace_name in search_url_dictionary:
            self.start_urls = [search_url_dictionary[marketplace_name][0].format(search_word=search_word)]
        else:
            self.logger.warning(f'Marketplace "{marketplace_name}", not exsit in search_url_dictionary. There is a need to add him to dictionary in order to search in {marketplace_name}')
            return
        
        self.count_pages = 0
        self.marketplace_name = marketplace_name
        
        # Create directory under the name '[marketplace_name]_[search_word]' to save JSON files
        self.directory_path = os.path.join(os.getcwd(), f"{marketplace_name}_{search_word}")
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
        
        
    def parse(self, response):
        """
        Parses a search results page, extracts individual item URLs 
        and invokes the `parse_item` method for each item. 
        Also identifies and follows the link to the next page if available.

        :param response: The content of the search results page.
        """
        self.count_pages += 1
           
        # Extract and follow item URLs
        item_urls = self.extract_data_safely(response, 1, "No item URLs CSS selector found for {marketplace}.")
        if item_urls:
            for item_url in item_urls:
                yield scrapy.Request(item_url, callback=self.parse_item)

        # Extract and follow next page URL
        next_page = self.extract_data_safely(response, 2, "No next page CSS selector found for {marketplace}.")
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_item(self, response):
        """
        Extracts product details from an item page, then saves the data as a JSON file.
        
        :param response: Content of the item page.
        """
        title = self.extract_data_safely(response, 4, "No title CSS selector found for {marketplace}.")
        price = self.extract_data_safely(response, 5, "No price CSS selector found for {marketplace}.")
        image = self.extract_data_safely(response, 6, "No image path CSS selector found for {marketplace}.")
        id = self.extract_data_safely(response, 7, "No product id CSS selector found for {marketplace}.")

        # Extract item description safely
        item_description_url = search_url_dictionary[self.marketplace_name][3].format(item_id=id)
        if item_description_url:
            description_response = requests.get(item_description_url)
            description_selector = scrapy.Selector(text=description_response.text)
            temp_description = description_selector.css('#ds_div *::text').getall()
            full_description = ' '.join(temp_description).strip()
        else:
            full_description = None
            self.logger.warning(f"No item CSS selector for description/ item number found for {self.marketplace_name}.")
        
        # Store the item details in a dictionary and save as JSON file
        item = {
            'title' : title,
            'description': full_description,
            'price': price,
            'image_path': image,
            'product_id': id
        }
        file_path = os.path.join(self.directory_path, f'{self.marketplace_name}_{id}.json')
        with open(file_path, 'w') as file:
            json.dump(item, file)
    
    
    def extract_data_safely(self, response, index, warning_message):
        """
        Safely extracts data from the given response using the CSS selector indexed from the dictionary. 
        Logs a warning if the selector is missing.
        
        :param response: Scrapy response object containing page content.
        :param index: Index in the dictionary to retrieve the CSS selector.
        :param warning_message: Message to log if the selector is missing.
        :return: Extracted data if the selector exists otherwise, None.
        """
        selector = search_url_dictionary[self.marketplace_name][index]
        if selector:
            return response.css(selector).getall() if index == 1 else response.css(selector).get()
        else:
            self.logger.warning(warning_message.format(marketplace=self.marketplace_name))
            return None

            
    