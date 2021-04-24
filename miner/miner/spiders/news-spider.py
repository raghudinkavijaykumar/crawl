import re

import scrapy


class NewsSpider(scrapy.Spider):
    name = "crawl"
    DATA_DIR = "data/news"

    def start_requests(self):
        urls = [
            'https://www.moneycontrol.com/news/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = re.sub(r"http:|https:", "", response.url)
        page = re.sub(r"/+", "-", page)
        page = re.sub("^-", "", page)
        page = re.sub("-$", "", page)
        filename = f'{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        next_page = response.css('a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
