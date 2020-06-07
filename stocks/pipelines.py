"""A set of pipelines."""
import collections
import typing
import urllib.parse

import bravado.client
import bravado.requests_client
import scrapy.exceptions

import stocks.items


ItemsType = typing.Dict[
    stocks.items.CollectionType, typing.List[stocks.items.BaseItem]]


class VerifyPipeline:
    """Pipeline that drops non-valid items."""

    def process_item(self, item, spider):
        """Drop items that have at least one empty field."""
        for value in item.values():
            if value is None:
                raise scrapy.exceptions.DropItem
        return item


class APIPipeline:
    """Pipline that persists crawled items with API."""

    def __init__(self, openapi_url: str, openapi_token: str):
        """Primary constructor."""
        http_client = bravado.requests_client.RequestsClient()
        http_client.set_api_key(
            host=urllib.parse.urlparse(openapi_url).netloc,
            api_key=openapi_token,
            param_name='X-Authorization',
            param_in='header',
        )

        self._api = bravado.client.SwaggerClient.from_url(  # type: ignore
            openapi_url, http_client=http_client)
        self._items: ItemsType = collections.defaultdict(list)

    @classmethod
    def from_settings(cls, settings):
        """Secondary constructor."""
        return cls(settings['OPENAPI_URL'], settings['OPENAPI_TOKEN'])

    def close_spider(self, spider):
        """Send crawled items to API."""
        for collection, items in self._items.items():
            payload = [{**item, 'source': spider.name} for item in items]

            if collection == stocks.items.CollectionType.tickers:
                future = self._api.crawler.import_tickers(payload=payload)
            elif collection == stocks.items.CollectionType.quotes:
                future = self._api.crawler.import_quotes(payload=payload)
            elif collection == stocks.items.CollectionType.payments:
                future = self._api.crawler.import_payments(payload=payload)
            else:
                raise Exception('API is not specidified for collection.')

            future.response()

    def process_item(self, item, spider):
        """Add crawled item to buffer."""
        self._items[item.collection].append(item)
        return item
