import os
import re
from pathlib import Path

import scrapy
from scrapy.linkextractors import LinkExtractor


class NewsSpider(scrapy.Spider):
    name = "crawl"
    DATA_DIR = "data/news"

    def start_requests(self):
        urls = [
            'https://www.moneycontrol.com/',
            'https://economictimes.indiatimes.com/',
            'https://www.livemint.com/',
            'https://www.financialexpress.com/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f'data/{self.urlToFile(response.url)}'
        Path(filename).parent.absolute().mkdir(parents=True, exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        next_page = LinkExtractor(deny_extensions=['html'])
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)

    def urlToFile(self, url):
        f = re.sub(r"http://|https://|\?", "", url)
        # TODO Handle this as a configuration based on file processing capability
        f = re.sub(
            r"\.(?!(html|htm|php|pdf|mp3|mp4|flv|mov|avi|doc|docx|xls|xlsx|md))", "-", f)
        if f[-1] == "/":
            return f + "index.html"
        if "." not in f:
            return f + ".html"
        else:
            return f
