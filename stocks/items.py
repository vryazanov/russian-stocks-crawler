"""Object pepresentations of scraped items."""
import scrapy


class StockItem(scrapy.Item):
    """Basic information about a stock."""

    name = scrapy.Field()
    ticker = scrapy.Field()


class PaymentItem(scrapy.Item):
    """Basic information about dividend payments."""

    ticker = scrapy.Field()
    date = scrapy.Field()
    payment = scrapy.Field()
