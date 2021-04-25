# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    path = scrapy.Field()
