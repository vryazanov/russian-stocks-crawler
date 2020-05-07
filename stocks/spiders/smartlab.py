"""Scrapy spider that can parse smart-lab.ru website."""
import scrapy

from stocks import items


class SmartlabSpider(scrapy.Spider):
    """Main spider."""

    name = 'smartlab'
    allowed_domains = ('smart-lab.ru',)
    start_urls = ('https://smart-lab.ru/q/shares/',)

    def parse(self, response):
        """Extract stocks from the list page."""
        names = response.xpath('//td[3]/a/text()').getall()
        tickers = response.xpath('//td[4]/text()').getall()

        for name, ticker in zip(names, tickers):
            yield items.StockItem(name=name, ticker=ticker)
