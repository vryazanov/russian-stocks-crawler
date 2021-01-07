"""A set of pipelines."""
import collections
import typing
import urllib.parse

import requests
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
        self._openapi_url = openapi_url
        self._openapi_token = openapi_token
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
                path = '/crawler/tickers'
            elif collection == stocks.items.CollectionType.payments:
                path = '/crawler/payments'
            else:
                raise Exception('API is not specidified for collection.')

            url = urllib.parse.urljoin(self._openapi_url, path)
            headers = {'Authorization': f'Bearer {self._openapi_token}'}

            requests.post(url, json=payload, headers=headers)

    def process_item(self, item, spider):
        """Add crawled item to buffer."""
        self._items[item.collection].append(item)
        return item
