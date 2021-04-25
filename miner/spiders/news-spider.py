import os
import re
from pathlib import Path
from urllib.parse import unquote

import scrapy
from miner.items import WebItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NewsSpider(scrapy.Spider):
    name = "miner"

    def start_requests(self):
        urls = [
            'https://www.moneycontrol.com/',
            'https://economictimes.indiatimes.com/',
            'https://www.livemint.com/',
            'https://www.financialexpress.com/'
        ]
        rules = (Rule(LinkExtractor(), callback='parse'),)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = LinkExtractor().extract_links(response)

        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_item)

    def parse_item(self, response):
        webItem = WebItem()
        webItem['url'] = response.url
        webItem['content'] = response.body
        webItem['path'] = f'data/{self.urlToFile(response.url)}'
        return webItem

    def urlToFile(self, url):
        url = unquote(url)
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
