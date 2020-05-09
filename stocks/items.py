"""Object pepresentations of scraped items."""
import scrapy


class StockItem(scrapy.Item):
    """Basic information about a stock."""

    collection = 'tickers'

    name = scrapy.Field()
    ticker = scrapy.Field()


class PaymentItem(scrapy.Item):
    """Basic information about dividend payments."""

    collection = 'payments'

    ticker = scrapy.Field()
    declaration_date = scrapy.Field()
    amount = scrapy.Field()
    is_forecast = scrapy.Field()
