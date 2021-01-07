"""Object pepresentations of scraped items."""
import abc
import enum

import scrapy


class CollectionType(str, enum.Enum):
    """Possible collection types."""

    tickers = 'tickers'
    payments = 'payments'
    quotes = 'quotes'


class BaseItem(scrapy.Item, metaclass=abc.ABCMeta):
    """Basic prototol for all item classes."""

    @abc.abstractproperty
    def collection(self) -> CollectionType:
        """Return a collection it belongs to."""


class StockItem(BaseItem):
    """Basic information about a stock."""

    collection = CollectionType.tickers

    name = scrapy.Field()
    code = scrapy.Field()


class StockQuoteItem(BaseItem):
    """Stock quote."""

    collection = CollectionType.quotes

    ticker = scrapy.Field()
    date = scrapy.Field()
    open_price = scrapy.Field()
    close_price = scrapy.Field()


class PaymentItem(BaseItem):
    """Basic information about dividend payments."""

    collection = CollectionType.payments

    ticker = scrapy.Field()
    date = scrapy.Field()
    amount = scrapy.Field()
    is_forecast = scrapy.Field()
