import scrapy
from scrapy.http import Request
import re


class Books1Spider(scrapy.Spider):
    name = "books1"
    start_urls = ["https://books.toscrape.com"]

    def start_requests(self):
        url = 'https://books.toscrape.com/catalogue/page-{page}.html'
        n_pages = 50

        for page in range(1, n_pages + 1):
            yield Request(url=url.format(page=page), callback=self.parse_product_urls)

    def parse_product_urls(self, response):
        product_links = response.xpath('//article[@class="product_pod"]//h3/a/@href').getall()

        for product_link in product_links:
            yield response.follow(response.urljoin(product_link), callback=self.parse_product_details)

    def convert_rating_to_numeric(self, raw_rating):
        rating_mapping = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
        }

        # Extract the word part of the rating
        rating_word = raw_rating.split()[-1]

        # Convert the word to its numerical value using the mapping dictionary
        numeric_rating = rating_mapping.get(rating_word, None)

        if numeric_rating is not None:
            return numeric_rating
        else:
            print("Unable to convert rating to numeric value.")
        return None    
    
    def parse_availability(self, availability):
        if availability:
            availability = availability.lower().strip()
            if "in stock" in availability:
                return "yes"
            else:
                return "no"
        else:
            return None
        
    def extract_integer_from_class(self, class_value):
        # Use regular expression to extract the integer from the class value
        rating_match = re.search(r'\d+', class_value)
        return int(rating_match.group()) if rating_match else None
    

    def parse_product_details(self, response):
        
        title = response.xpath('//h1/text()').get()
        category = response.xpath('//ul[@class="breadcrumb"]//li[3]/a/text()').get()
        price = response.xpath('//p[@class="price_color"]/text()').get()
        availability = response.xpath('//th[contains(text(), "Availability")]/following-sibling::td/text()').get()
        quantity = availability
        rating = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        upc = response.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get()
        product_type = response.xpath('//th[contains(text(), "Product Type")]/following-sibling::td/text()').get()
        price_with_tax = response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td/text()').get()
        price_no_tax = response.xpath('//th[contains(text(), "Price (excl. tax)")]/following-sibling::td/text()').get()
        tax = response.xpath('//th[contains(text(), "Tax")]/following-sibling::td/text()').get()
        url = response.url

        yield {'title': title, 'category': category, 'price': price, 'availabiliy': self.parse_availability(availability), 'quantity': self.extract_integer_from_class(quantity), 
              'rating': self.convert_rating_to_numeric(rating), 'description': description, 'upc': upc, 'product_type': product_type, 
              'price_with_tax': price_with_tax, 'price_no_tax': price_no_tax, 'tax': tax, 'url': url}
        




        
