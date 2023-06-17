import scrapy # for web scraping
import pandas as pd #for data manipulation
from scrapy.crawler import CrawlerProcess #running the crawler
from scrapy.exceptions import DropItem #for handling items to be dropped during processing 

class QuoteSpider(scrapy.Spider):
    name = 'quote-spider' #defining the spider's name to uniquely identify it 

    custom_settings = {
        'ITEM_PIPELINES': {'__main__.ExcelPipeline': 100}  # Use the custom ExcelPipeline for processing and override the default settings of the spider 
    }

    def start_requests(self):
        url = input("Enter the website URL: ")
        yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1})  # initial depth set to 1 using meta parameter, specifying parse method as the callback function to handle the response

    def parse(self, response):
        # Extract internal links
        internal_links = response.css('a::attr(href)').getall()  # <a> tags represent internal links, extract all internal links using CSS selector 

        # Process each internal link
        for link in internal_links:
            # Check if it's an internal link
            if link.startswith('/') or response.url in link: #check if the link starts with a slash or if the response URL is present in the link 
                # Construct the absolute URL using the internal link
                absolute_url = response.urljoin(link)

                # Create a dictionary item
                item = {'internal_link': absolute_url}

                # Yield the item to the item pipeline
                yield item

                # Get the current depth from meta
                depth = response.meta['depth']

                # Check if the depth is less than or equal to 10
                if depth <= 10:
                    # Recursive call to follow the internal link with incremented depth
                    yield response.follow(absolute_url, callback=self.parse, meta={'depth': depth + 1})

class ExcelPipeline: #custom pipeline to process the items extracted by the spider 
    def __init__(self): #initializing an empty list items to store the extracted items 
        self.items = []

    def close_spider(self, spider): #called when the spider finishes, convert the items list to a pandas dataframe and save it to an excel file 
        df = pd.DataFrame(self.items)
        df.to_excel('extracted_links.xlsx', index=False)

    def process_item(self, item, spider): #The process_item method is called for each item extracted by the spider. If the item has a valid 'internal_link' field, we append it to the items list. Otherwise, we raise a DropItem exception to discard the item.
        if item['internal_link']:
            self.items.append(item)
            return item
        else:
            raise DropItem("Missing internal_link field in item")

# Create a CrawlerProcess instance
process = CrawlerProcess()

# Add the spider to the process
process.crawl(QuoteSpider)

# Start the process
process.start()








    