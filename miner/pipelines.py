# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
from pathlib import Path

from bs4 import BeautifulSoup
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class HtmlToTextPipeline:

    name = "HtmlToTextPipeline"

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        content = adapter.get('content')
        url = adapter.get('url')
        path = adapter.get('path')

        if content:
            self.log(f"Processing Item {adapter.get('url')}", logging.INFO)
            content = BeautifulSoup(
                content, 'html.parser').get_text()
            Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding="utf-8") as f:
                f.write(content)
                self.log(f'Saved file {path}', logging.INFO)
            return item
        else:
            raise DropItem(f"Missing content in {url}")

    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)
