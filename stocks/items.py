"""Object pepresentations of scraped items."""
import abc

import scrapy


class BaseItem(scrapy.Item, metaclass=abc.ABCMeta):
    """Basic prototol for all item classes."""

    @abc.abstractproperty
    def collection(self) -> str:
        """Return a collection it belongs to."""


class StockItem(BaseItem):
    """Basic information about a stock."""

    collection = 'tickers'

    name = scrapy.Field()
    ticker = scrapy.Field()


class PaymentItem(BaseItem):
    """Basic information about dividend payments."""

    collection = 'payments'

    ticker = scrapy.Field()
    declaration_date = scrapy.Field()
    amount = scrapy.Field()
    is_forecast = scrapy.Field()
