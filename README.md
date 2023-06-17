# Website-crawling-with-scrapy

This project demonstrates web scraping and website crawling using Scrapy, a powerful Python framework for extracting data from websites. The goal of this project is to crawl a given website and extract internal links, storing them in an Excel file.

Overview

Website crawling involves navigating through web pages and extracting specific information or links for further analysis or data processing. In this project, Scrapy is used to crawl a website and extract internal links. The project follows these steps:

Spider Definition: A Scrapy spider named quote-spider is defined. The spider starts by taking a website URL as input and then crawls the website to extract internal links.

Custom Settings: The spider has custom settings defined to override the default pipeline. The custom pipeline, ExcelPipeline, is used to process the extracted items.

Starting Requests: The spider's start_requests method prompts the user to enter the website URL. It then initiates the crawling process by sending a request to the specified URL and calling the parse method to handle the response.

Parsing: The parse method extracts internal links from the response using CSS selectors. It processes each internal link by constructing the absolute URL, creating an item, and yielding it to the item pipeline. The method also checks the depth of the crawling process and recursively follows internal links if the depth is within the specified limit (10 in this case).

Item Pipeline: The custom pipeline, ExcelPipeline, is responsible for processing the extracted items. It initializes an empty list to store the items, appends valid items with an 'internal_link' field, and raises a DropItem exception for items without the 'internal_link' field. When the spider finishes, the close_spider method converts the list of items to a pandas DataFrame and saves it to an Excel file named extracted_links.xlsx.

Dependencies

The project relies on the following dependencies:

scrapy: A Python framework for web scraping and website crawling.

pandas: A data manipulation library used for storing the extracted links in a pandas DataFrame.

xlrd: A library for reading data and formatting information from Excel files.

openpyxl: A library for reading and writing Excel files.
