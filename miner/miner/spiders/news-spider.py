import re

import scrapy
from scrapy.linkextractors import LinkExtractor


class NewsSpider(scrapy.Spider):
    name = "crawl"
    DATA_DIR = "data/news"

    def start_requests(self):
        urls = [
            'https://www.moneycontrol.com/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = re.sub(r"http:|https:", "", response.url)
        page = re.sub(r"/+", "-", page)
        page = re.sub("^-", "", page)
        page = re.sub("-$", "", page)
        filename = f'data/news/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        next_page = LinkExtractor()
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)
