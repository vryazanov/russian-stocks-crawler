"""Object pepresentations of scraped items."""
import scrapy


class StockItem(scrapy.Item):
    """Base information about a stock."""

    name = scrapy.Field()
    ticker = scrapy.Field()
